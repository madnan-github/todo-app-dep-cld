"""Dapr client for interacting with Dapr services."""
import aiohttp
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DaprClient:
    def __init__(self, dapr_http_port: int = 3500, dapr_grpc_port: int = 50001):
        self.dapr_http_port = dapr_http_port
        self.dapr_grpc_port = dapr_grpc_port
        self.base_url = f"http://localhost:{dapr_http_port}"

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[Any, Any]):
        """Publish an event to a Dapr pub/sub component."""
        url = f"{self.base_url}/v1.0/publish/{pubsub_name}/{topic_name}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        logger.info(f"Successfully published event to {pubsub_name}/{topic_name}")
                    else:
                        logger.error(f"Failed to publish event: {response.status} - {await response.text()}")
                        raise Exception(f"Failed to publish event: {response.status}")
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            raise

    async def get_state(self, store_name: str, key: str) -> Optional[Dict[Any, Any]]:
        """Get state from a Dapr state store."""
        url = f"{self.base_url}/v1.0/state/{store_name}/{key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Retrieved state for key {key} from {store_name}")
                        return data
                    elif response.status == 404:
                        logger.info(f"State not found for key {key} in {store_name}")
                        return None
                    else:
                        logger.error(f"Failed to get state: {response.status} - {await response.text()}")
                        raise Exception(f"Failed to get state: {response.status}")
        except Exception as e:
            logger.error(f"Error getting state: {e}")
            raise

    async def save_state(self, store_name: str, key: str, value: Dict[Any, Any]):
        """Save state to a Dapr state store."""
        url = f"{self.base_url}/v1.0/state/{store_name}"
        
        state_item = {
            "key": key,
            "value": value
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=[state_item]) as response:
                    if response.status == 200 or response.status == 204:
                        logger.info(f"Successfully saved state for key {key} in {store_name}")
                    else:
                        logger.error(f"Failed to save state: {response.status} - {await response.text()}")
                        raise Exception(f"Failed to save state: {response.status}")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            raise

    async def invoke_service(self, app_id: str, method: str, data: Optional[Dict[Any, Any]] = None):
        """Invoke a method on another Dapr service."""
        url = f"{self.base_url}/v1.0/invoke/{app_id}/method/{method}"
        
        try:
            async with aiohttp.ClientSession() as session:
                if data:
                    async with session.post(url, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            logger.info(f"Successfully invoked {app_id}/{method}")
                            return result
                        else:
                            logger.error(f"Failed to invoke service: {response.status} - {await response.text()}")
                            raise Exception(f"Failed to invoke service: {response.status}")
                else:
                    async with session.get(url) as response:
                        if response.status == 200:
                            result = await response.json()
                            logger.info(f"Successfully invoked {app_id}/{method}")
                            return result
                        else:
                            logger.error(f"Failed to invoke service: {response.status} - {await response.text()}")
                            raise Exception(f"Failed to invoke service: {response.status}")
        except Exception as e:
            logger.error(f"Error invoking service: {e}")
            raise

    async def get_secret(self, store_name: str, key: str) -> Optional[str]:
        """Get a secret from a Dapr secret store."""
        url = f"{self.base_url}/v1.0/secrets/{store_name}/{key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        secrets = await response.json()
                        logger.info(f"Retrieved secret {key} from {store_name}")
                        return secrets.get(key)
                    elif response.status == 404:
                        logger.info(f"Secret {key} not found in {store_name}")
                        return None
                    else:
                        logger.error(f"Failed to get secret: {response.status} - {await response.text()}")
                        raise Exception(f"Failed to get secret: {response.status}")
        except Exception as e:
            logger.error(f"Error getting secret: {e}")
            raise