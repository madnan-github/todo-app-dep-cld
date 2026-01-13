import logging
import sys
from datetime import datetime
from typing import Optional

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

# Create logger for the application
logger = logging.getLogger(__name__)

def log_request(user_id: str, endpoint: str, method: str, duration: Optional[float] = None):
    """Log API request information"""
    if duration:
        logger.info(f"USER:{user_id} - {method} {endpoint} - {duration:.2f}s")
    else:
        logger.info(f"USER:{user_id} - {method} {endpoint}")

def log_ai_interaction(user_id: str, conversation_id: int, input_text: str, output_text: str):
    """Log AI interaction for monitoring and debugging"""
    logger.info(f"AI_INTERACTION - USER:{user_id} - CONV:{conversation_id} - IN:'{input_text[:50]}...' - OUT:'{output_text[:50]}...'")

def log_tool_execution(user_id: str, tool_name: str, success: bool, execution_time: Optional[float] = None):
    """Log tool execution"""
    status = "SUCCESS" if success else "FAILED"
    if execution_time:
        logger.info(f"TOOL_EXEC - USER:{user_id} - TOOL:{tool_name} - {status} - {execution_time:.2f}s")
    else:
        logger.info(f"TOOL_EXEC - USER:{user_id} - TOOL:{tool_name} - {status}")

def log_error(error_msg: str, user_id: Optional[str] = None, context: Optional[str] = None):
    """Log error with optional user and context information"""
    if context:
        logger.error(f"ERROR - USER:{user_id or 'UNKNOWN'} - CONTEXT:{context} - {error_msg}")
    else:
        logger.error(f"ERROR - USER:{user_id or 'UNKNOWN'} - {error_msg}")