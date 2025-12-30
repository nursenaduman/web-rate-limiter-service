import time
import logging  
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from app.config import RATE_LIMIT, WINDOW_SECONDS

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        # Her IP için istek zamanlarını tutar
        self.requests = defaultdict(deque)

    def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        window_start = current_time - WINDOW_SECONDS

        request_times = self.requests[client_ip]

        # Süresi dolan istekleri temizle
        while request_times and request_times[0] < window_start:
            request_times.popleft()

        if len(request_times) >= RATE_LIMIT:
            logger.warning(f"⛔ RATE LIMIT AŞILDI - IP: {client_ip} engellendi.")
            return False

        request_times.append(current_time)
        return True


rate_limiter = RateLimiter()


async def rate_limit_dependency(request: Request):
    client_ip = request.client.host

    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )