import pytest
from backend.security import SecurityService
from backend.models import User

@pytest.fixture
def security_service():
    return SecurityService("test_secret_key", "redis://localhost")

def test_encryption():
    service = security_service()
    test_data = "données sensibles"
    encrypted = service.encrypt_data(test_data)
    decrypted = service.decrypt_data(encrypted)
    assert decrypted == test_data

@pytest.mark.asyncio
async def test_rate_limiting():
    service = security_service()
    with pytest.raises(RateLimitException):
        for _ in range(101):  # Dépasse la limite de 100
            await service.rate_limit_check("test_user") 