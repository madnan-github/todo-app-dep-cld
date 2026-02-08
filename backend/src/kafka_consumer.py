"""Kafka consumer for task events."""
import asyncio
import json
from aiokafka import AIOKafkaConsumer
import logging

logger = logging.getLogger(__name__)

class KafkaTaskConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.started = False

    async def start(self, topics: list):
        """Initialize and start the Kafka consumer."""
        if not self.started:
            try:
                self.consumer = AIOKafkaConsumer(
                    *topics,
                    bootstrap_servers=self.bootstrap_servers,
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None,
                    auto_offset_reset="earliest",
                    enable_auto_commit=True
                )
                await self.consumer.start()
                self.started = True
                logger.info(f"Kafka consumer started successfully for topics: {topics}")
            except Exception as e:
                logger.error(f"Failed to start Kafka consumer: {e}")
                raise

    async def stop(self):
        """Stop the Kafka consumer."""
        if self.consumer and self.started:
            await self.consumer.stop()
            self.started = False
            logger.info("Kafka consumer stopped")

    async def consume_events(self):
        """Consume events from Kafka topics."""
        if not self.started:
            raise RuntimeError("Consumer not started. Call start() first.")
        
        try:
            async for msg in self.consumer:
                logger.info(f"Consumed message from topic {msg.topic}, partition {msg.partition}: {msg.value}")
                
                # Process the message based on topic
                if msg.topic == "task-reminders":
                    await self.handle_reminder_event(msg.value)
                elif msg.topic == "task-recurring":
                    await self.handle_recurring_task_event(msg.value)
                elif msg.topic == "task-audit":
                    await self.handle_audit_event(msg.value)
                elif msg.topic.startswith("task-"):
                    await self.handle_general_task_event(msg.value)
                    
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise

    async def handle_reminder_event(self, message: dict):
        """Handle reminder events."""
        logger.info(f"Handling reminder event: {message}")
        # In a real implementation, this would trigger notifications to users
        # For now, we'll just log the event
        task_id = message.get("task_id")
        user_id = message.get("user_id")
        due_date = message.get("due_date")
        
        print(f"REMINDER: Task {task_id} for user {user_id} is due on {due_date}")

    async def handle_recurring_task_event(self, message: dict):
        """Handle recurring task events."""
        logger.info(f"Handling recurring task event: {message}")
        # In a real implementation, this would create the next instance of a recurring task
        # For now, we'll just log the event
        task_id = message.get("task_id")
        user_id = message.get("user_id")
        next_occurrence = message.get("next_occurrence")
        
        print(f"RECURRING: Creating next instance for task {task_id} for user {user_id} on {next_occurrence}")

    async def handle_audit_event(self, message: dict):
        """Handle audit events."""
        logger.info(f"Handling audit event: {message}")
        # In a real implementation, this would store audit logs
        # For now, we'll just log the event
        task_id = message.get("task_id")
        user_id = message.get("user_id")
        action = message.get("action")
        
        print(f"AUDIT: Action '{action}' performed on task {task_id} by user {user_id}")

    async def handle_general_task_event(self, message: dict):
        """Handle general task events."""
        logger.info(f"Handling general task event: {message}")
        # Handle other task-related events
        task_id = message.get("task_id")
        event_type = message.get("event_type")
        
        print(f"TASK EVENT: {event_type} for task {task_id}")