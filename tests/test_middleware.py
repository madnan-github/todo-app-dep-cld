import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.middleware import RateLimiter


def test_rate_limiter_initialization():
    """Test rate limiter initialization."""
    rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
    assert rate_limiter.max_requests == 10
    assert rate_limiter.window_seconds == 60
    assert rate_limiter.requests == {}


def test_rate_limiter_is_rate_limited():
    """Test rate limiting logic."""
    rate_limiter = RateLimiter(max_requests=2, window_seconds=1)
    
    # Mock request object
    mock_request = MagicMock()
    mock_request.client.host = "127.0.0.1"
    
    # First request should not be limited
    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(mock_request)
    assert not is_limited
    assert remaining == 1
    
    # Second request should not be limited
    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(mock_request)
    assert not is_limited
    assert remaining == 0
    
    # Third request should be limited
    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(mock_request)
    assert is_limited


def test_rate_limiter_cleanup():
    """Test cleanup of old requests."""
    rate_limiter = RateLimiter(max_requests=10, window_seconds=1)
    
    # Add a request
    mock_request = MagicMock()
    mock_request.client.host = "127.0.0.1"
    
    rate_limiter.is_rate_limited(mock_request)
    
    # Manually set a request time in the past
    client_ip = "127.0.0.1"
    if client_ip in rate_limiter.requests:
        rate_limiter.requests[client_ip][0] = 0  # Set to epoch time (very old)
    
    # After cleanup, old requests should be removed
    is_limited, remaining, reset_time = rate_limiter.is_rate_limited(mock_request)
    # Should not be limited since old request was cleaned up
    assert not is_limited


def test_rate_limiter_different_ips():
    """Test rate limiting for different IP addresses."""
    rate_limiter = RateLimiter(max_requests=1, window_seconds=60)
    
    # Mock requests from different IPs
    mock_request1 = MagicMock()
    mock_request1.client.host = "127.0.0.1"
    
    mock_request2 = MagicMock()
    mock_request2.client.host = "127.0.0.2"
    
    # Both should be allowed since they're from different IPs
    is_limited1, _, _ = rate_limiter.is_rate_limited(mock_request1)
    is_limited2, _, _ = rate_limiter.is_rate_limited(mock_request2)
    
    assert not is_limited1
    assert not is_limited2


def test_rate_limiter_window_reset():
    """Test that requests are properly reset after window period."""
    rate_limiter = RateLimiter(max_requests=1, window_seconds=0.1)  # Very short window
    
    mock_request = MagicMock()
    mock_request.client.host = "127.0.0.1"
    
    # First request should be allowed
    is_limited, _, _ = rate_limiter.is_rate_limited(mock_request)
    assert not is_limited
    
    # Second request should be limited
    is_limited, _, _ = rate_limiter.is_rate_limited(mock_request)
    assert is_limited
    
    # Wait for window to reset (manually adjust the time records)
    import time
    current_time = time.time()
    client_ip = "127.0.0.1"
    if client_ip in rate_limiter.requests:
        # Set the request time to be outside the window
        rate_limiter.requests[client_ip] = [current_time - 0.2]  # Older than window
    
    # Now the request should be allowed again
    is_limited, _, _ = rate_limiter.is_rate_limited(mock_request)
    assert not is_limited


if __name__ == "__main__":
    pytest.main([__file__])