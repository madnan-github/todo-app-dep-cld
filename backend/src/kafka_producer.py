"""Kafka producer for task events."""
import asyncio
import json
from typing import Dict, Any
from aiokafka import AIOKafkaProducer
import logging

logger = logging.getLogger(__name__)

class KafkaTaskProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.started = False

    async def start(self):
        """Initialize and start the Kafka producer."""
        if not self.started:
            try:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=str.encode
                )
                await self.producer.start()
                self.started = True
                logger.info("Kafka producer started successfully")
            except Exception as e:
                logger.error(f"Failed to start Kafka producer: {e}")
                raise

    async def stop(self):
        """Stop the Kafka producer."""
        if self.producer and self.started:
            await self.producer.stop()
            self.started = False
            logger.info("Kafka producer stopped")

    async def send_task_event(self, topic: str, task_id: int, event_type: str, payload: Dict[Any, Any]):
        """Send a task event to Kafka."""
        if not self.started:
            await self.start()

        try:
            key = f"task_{task_id}"
            message = {
                "task_id": task_id,
                "event_type": event_type,
                "payload": payload,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            await self.producer.send_and_wait(topic, value=message, key=key)
            logger.info(f"Sent {event_type} event for task {task_id} to topic {topic}")
        except Exception as e:
            logger.error(f"Failed to send {event_type} event for task {task_id}: {e}")
            raise

    async def send_reminder_event(self, task_id: int, user_id: str, due_date: str):
        """Send a reminder event to Kafka."""
        payload = {
            "task_id": task_id,
            "user_id": user_id,
            "due_date": due_date,
            "action": "send_notification"
        }
        await self.send_task_event("task-reminders", task_id, "reminder", payload)

    async def send_recurring_task_event(self, task_id: int, user_id: str, next_occurrence: str):
        """Send a recurring task event to Kafka."""
        payload = {
            "task_id": task_id,
            "user_id": user_id,
            "next_occurrence": next_occurrence,
            "action": "create_next_instance"
        }
        await self.send_task_event("task-recurring", task_id, "recurring", payload)

    async def send_audit_event(self, task_id: int, user_id: str, action: str, details: Dict[Any, Any]):
        """Send an audit event to Kafka."""
        payload = {
            "task_id": task_id,
            "user_id": user_id,
            "action": action,
            "details": details
        }
        await self.send_task_event("task-audit", task_id, "audit", payload)