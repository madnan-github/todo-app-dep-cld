import time
import functools
from typing import Callable, Any
from .logging_config import logger

class PerformanceMonitor:
    """Monitor API performance and track response times"""

    def __init__(self):
        self.metrics = {}

    def measure_time(self, func_name: str = None):
        """Decorator to measure execution time of functions"""
        def decorator(func: Callable) -> Callable:
            nonlocal func_name
            if not func_name:
                func_name = func.__name__

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    duration = end_time - start_time

                    # Log the performance metric
                    logger.info(f"PERFORMANCE - FUNCTION:{func_name} - DURATION:{duration:.3f}s")

                    # Store in metrics for monitoring
                    if func_name not in self.metrics:
                        self.metrics[func_name] = []
                    self.metrics[func_name].append(duration)

                    # Check if response time exceeds threshold (5s as per SC-003)
                    if duration > 5.0:
                        logger.warning(f"PERFORMANCE WARNING - FUNCTION:{func_name} - SLOW_RESPONSE:{duration:.3f}s")

            return wrapper
        return decorator

    def get_average_response_time(self, func_name: str) -> float:
        """Get average response time for a specific function"""
        if func_name in self.metrics and self.metrics[func_name]:
            return sum(self.metrics[func_name]) / len(self.metrics[func_name])
        return 0.0

    def get_slow_requests_count(self, func_name: str, threshold: float = 5.0) -> int:
        """Get count of requests that took longer than threshold"""
        if func_name in self.metrics:
            return len([t for t in self.metrics[func_name] if t > threshold])
        return 0

# Global performance monitor instance
perf_monitor = PerformanceMonitor()

# Decorator for easy use
def monitor_performance(func_name: str = None):
    """Convenience decorator to monitor performance"""
    return perf_monitor.measure_time(func_name)