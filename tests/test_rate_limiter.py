import time
from app.rate_limiter import RateLimiter
from app.config import RATE_LIMIT, WINDOW_SECONDS


def test_allows_requests_under_limit():
    limiter = RateLimiter()
    ip = "127.0.0.1"

    for _ in range(RATE_LIMIT):
        assert limiter.is_allowed(ip) is True


def test_blocks_request_over_limit():
    limiter = RateLimiter()
    ip = "127.0.0.1"

    for _ in range(RATE_LIMIT):
        limiter.is_allowed(ip)

    assert limiter.is_allowed(ip) is False


def test_different_ips_have_separate_limits():
    limiter = RateLimiter()

    ip1 = "127.0.0.1"
    ip2 = "192.168.1.1"

    for _ in range(RATE_LIMIT):
        assert limiter.is_allowed(ip1) is True

    # Diğer IP hala serbest
    assert limiter.is_allowed(ip2) is True


def test_limit_resets_after_time_window():
    limiter = RateLimiter()
    ip = "127.0.0.1"

    for _ in range(RATE_LIMIT):
        limiter.is_allowed(ip)

    # Limit dolu
    assert limiter.is_allowed(ip) is False

    # Zaman penceresini geç
    time.sleep(WINDOW_SECONDS + 1)

    # Tekrar izin verilmeli
    assert limiter.is_allowed(ip) is True


def test_requests_are_tracked_independently():
    limiter = RateLimiter()
    ip = "127.0.0.1"

    limiter.is_allowed(ip)
    limiter.is_allowed(ip)

    # Henüz limit dolmadı
    assert limiter.is_allowed(ip) is True
