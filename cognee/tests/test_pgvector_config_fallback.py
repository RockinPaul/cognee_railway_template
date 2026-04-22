import importlib
from types import SimpleNamespace

create_db_and_tables = importlib.import_module(
    "cognee.infrastructure.databases.vector.pgvector.create_db_and_tables"
)


def test_pgvector_admin_config_falls_back_to_relational_values():
    vector_config = {
        "vector_db_provider": "pgvector",
        "vector_db_url": "postgresql://postgres:secret@postgres.railway.internal:5432/railway",
        "vector_db_name": "dataset-id",
        "vector_db_port": 1234,
        "vector_db_username": "",
        "vector_db_password": "",
        "vector_db_host": "",
        "vector_dataset_database_handler": "pgvector",
    }
    relational_config = SimpleNamespace(
        db_host="postgres.railway.internal",
        db_port=5432,
        db_username="postgres",
        db_password="secret",
    )

    result = create_db_and_tables._apply_relational_fallback(vector_config, relational_config)

    assert result["vector_db_host"] == "postgres.railway.internal"
    assert result["vector_db_port"] == 5432
    assert result["vector_db_username"] == "postgres"
    assert result["vector_db_password"] == "secret"


def test_pgvector_admin_config_preserves_explicit_vector_values():
    vector_config = {
        "vector_db_provider": "pgvector",
        "vector_db_url": "postgresql://postgres:secret@postgres.railway.internal:5432/railway",
        "vector_db_name": "dataset-id",
        "vector_db_port": 6543,
        "vector_db_username": "vector_user",
        "vector_db_password": "vector_pass",
        "vector_db_host": "vector.internal",
        "vector_dataset_database_handler": "pgvector",
    }
    relational_config = SimpleNamespace(
        db_host="postgres.railway.internal",
        db_port=5432,
        db_username="postgres",
        db_password="secret",
    )

    result = create_db_and_tables._apply_relational_fallback(vector_config, relational_config)

    assert result["vector_db_host"] == "vector.internal"
    assert result["vector_db_port"] == 6543
    assert result["vector_db_username"] == "vector_user"
    assert result["vector_db_password"] == "vector_pass"
