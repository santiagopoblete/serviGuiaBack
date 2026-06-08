import pytest
from database import ping_db

@pytest.mark.asyncio
async def test_mongo_connection():
    result = await ping_db()
    assert result["ok"] == 1.0