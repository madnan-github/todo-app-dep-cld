"""Background tasks for handling recurring tasks and reminders."""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging

from src.models import Task, TaskEvent
from src.database import get_session, DATABASE_URL
from src.kafka_producer import KafkaTaskProducer

logger = logging.getLogger(__name__)

class BackgroundTaskManager:
    def __init__(self, kafka_producer: KafkaTaskProducer):
        self.kafka_producer = kafka_producer
        self.running = False
        self.engine = create_async_engine(DATABASE_URL)

    async def start(self):
        """Start the background task manager."""
        self.running = True
        logger.info("Background task manager started")
        
        # Start the background tasks
        asyncio.create_task(self.process_due_reminders())
        asyncio.create_task(self.process_recurring_tasks())
        asyncio.create_task(self.process_task_events())

    async def stop(self):
        """Stop the background task manager."""
        self.running = False
        logger.info("Background task manager stopped")

    async def process_due_reminders(self):
        """Process tasks that have due dates approaching."""
        while self.running:
            try:
                async with AsyncSession(self.engine) as session:
                    # Find tasks with due dates within the next hour that haven't had reminders sent
                    now = datetime.utcnow()
                    one_hour_later = now + timedelta(hours=1)
                    
                    stmt = select(Task).where(
                        Task.due_date.between(now, one_hour_later),
                        Task.reminder_sent == False,
                        Task.completed == False
                    )
                    
                    result = await session.execute(stmt)
                    due_tasks = result.scalars().all()
                    
                    for task in due_tasks:
                        # Send reminder event via Kafka
                        await self.kafka_producer.send_reminder_event(
                            task.id,
                            task.user_id,
                            task.due_date.isoformat() if task.due_date else None
                        )
                        
                        # Update task to mark reminder as sent
                        task.reminder_sent = True
                        await session.commit()
                        
                        logger.info(f"Reminder sent for task {task.id}")
                        
            except Exception as e:
                logger.error(f"Error processing due reminders: {e}")
            
            # Wait 5 minutes before checking again
            await asyncio.sleep(300)

    async def process_recurring_tasks(self):
        """Process recurring tasks to create new instances."""
        while self.running:
            try:
                async with AsyncSession(self.engine) as session:
                    # Find recurring tasks whose next occurrence date has arrived
                    now = datetime.utcnow()
                    
                    stmt = select(Task).where(
                        Task.is_recurring == True,
                        Task.next_occurrence <= now,
                        Task.completed == False
                    ).options(selectinload(Task.child_tasks))
                    
                    result = await session.execute(stmt)
                    recurring_tasks = result.scalars().all()
                    
                    for task in recurring_tasks:
                        # Send recurring task event via Kafka
                        await self.kafka_producer.send_recurring_task_event(
                            task.id,
                            task.user_id,
                            task.next_occurrence.isoformat() if task.next_occurrence else None
                        )
                        
                        # Update the next occurrence date
                        from src.routes.tasks import calculate_next_occurrence
                        new_next_occurrence = calculate_next_occurrence(
                            task.next_occurrence,
                            task.recurrence_pattern,
                            task.recurrence_interval
                        )
                        task.next_occurrence = new_next_occurrence
                        
                        await session.commit()
                        
                        logger.info(f"Processed recurring task {task.id}, next occurrence: {new_next_occurrence}")
                        
            except Exception as e:
                logger.error(f"Error processing recurring tasks: {e}")
            
            # Wait 10 minutes before checking again
            await asyncio.sleep(600)

    async def process_task_events(self):
        """Process task events that need to be sent to Kafka."""
        while self.running:
            try:
                async with AsyncSession(self.engine) as session:
                    # Find unprocessed task events
                    stmt = select(TaskEvent).where(TaskEvent.processed == False)
                    
                    result = await session.execute(stmt)
                    unprocessed_events = result.scalars().all()
                    
                    for event in unprocessed_events:
                        # Parse the payload
                        import json
                        payload = json.loads(event.payload)
                        
                        # Send the event to the appropriate Kafka topic
                        if event.event_type == "reminder":
                            await self.kafka_producer.send_reminder_event(
                                event.task_id,
                                payload.get("user_id"),
                                payload.get("due_date")
                            )
                        elif event.event_type == "recurring":
                            await self.kafka_producer.send_recurring_task_event(
                                event.task_id,
                                payload.get("user_id"),
                                payload.get("next_occurrence")
                            )
                        elif event.event_type == "audit":
                            await self.kafka_producer.send_audit_event(
                                event.task_id,
                                payload.get("user_id"),
                                payload.get("action"),
                                payload.get("details", {})
                            )
                        else:
                            # Send to general task events topic
                            await self.kafka_producer.send_task_event(
                                "task-events",
                                event.task_id,
                                event.event_type,
                                payload
                            )
                        
                        # Mark the event as processed
                        event.processed = True
                        await session.commit()
                        
                        logger.info(f"Processed task event {event.id} of type {event.event_type}")
                        
            except Exception as e:
                logger.error(f"Error processing task events: {e}")
            
            # Wait 30 seconds before checking again
            await asyncio.sleep(30)