import pytest
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from cognee.api.v1.health.health import HealthChecker, HealthStatus


@pytest.mark.asyncio
async def test_check_graph_db_uses_is_empty_for_postgres_backends():
    checker = HealthChecker()
    engine = SimpleNamespace(
        is_empty=AsyncMock(return_value=True),
        query=AsyncMock(side_effect=NotImplementedError("raw Cypher unsupported")),
    )
    config = SimpleNamespace(graph_database_provider="postgres")

    with (
        patch(
            "cognee.infrastructure.databases.graph.get_graph_engine.get_graph_engine",
            AsyncMock(return_value=engine),
        ),
        patch(
            "cognee.infrastructure.databases.graph.config.get_graph_config",
            return_value=config,
        ),
    ):
        result = await checker.check_graph_db()

    assert result.status == HealthStatus.HEALTHY
    assert result.provider == "postgres"
    engine.is_empty.assert_awaited_once()
    engine.query.assert_not_called()


@pytest.mark.asyncio
async def test_check_relational_db_does_not_call_close_inside_managed_session():
    checker = HealthChecker()
    session = SimpleNamespace(execute=AsyncMock(return_value=None), close=AsyncMock())
    config = SimpleNamespace(db_provider="postgres")

    @asynccontextmanager
    async def fake_get_async_session():
        yield session

    engine = SimpleNamespace(get_async_session=fake_get_async_session)

    with (
        patch(
            "cognee.infrastructure.databases.relational.get_relational_engine.get_relational_engine",
            return_value=engine,
        ),
        patch(
            "cognee.infrastructure.databases.relational.config.get_relational_config",
            return_value=config,
        ),
    ):
        result = await checker.check_relational_db()

    assert result.status == HealthStatus.HEALTHY
    assert result.provider == "postgres"
    session.execute.assert_awaited_once()
    session.close.assert_not_called()
