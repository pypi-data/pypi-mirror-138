"""
Injected database interface dependencies
"""
import inspect
from contextlib import contextmanager
from functools import wraps

MODELS_DEPENDENCIES = {
    "database_config": None,
    "query_components": None,
    "orm": None,
}


def provide_database_interface():
    from prefect.orion.database.interface import OrionDBInterface

    database_config = MODELS_DEPENDENCIES.get("database_config")
    query_components = MODELS_DEPENDENCIES.get("query_components")
    orm = MODELS_DEPENDENCIES.get("orm")

    if database_config is None:
        import prefect.settings
        from prefect.orion.database.configurations import (
            AioSqliteConfiguration,
            AsyncPostgresConfiguration,
        )
        from prefect.orion.utilities.database import get_dialect

        dialect = get_dialect()
        connection_url = prefect.settings.from_env().orion.database.connection_url

        if dialect.name == "postgresql":
            database_config = AsyncPostgresConfiguration(connection_url=connection_url)
        elif dialect.name == "sqlite":
            database_config = AioSqliteConfiguration(connection_url=connection_url)
        else:
            raise ValueError(
                f"Unable to infer database configuration from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["database_config"] = database_config

    if query_components is None:
        from prefect.orion.database.query_components import (
            AioSqliteQueryComponents,
            AsyncPostgresQueryComponents,
        )
        from prefect.orion.utilities.database import get_dialect

        dialect = get_dialect()

        if dialect.name == "postgresql":
            query_components = AsyncPostgresQueryComponents()
        elif dialect.name == "sqlite":
            query_components = AioSqliteQueryComponents()
        else:
            raise ValueError(
                f"Unable to infer query components from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["query_components"] = query_components

    if orm is None:
        from prefect.orion.database.orm_models import (
            AioSqliteORMConfiguration,
            AsyncPostgresORMConfiguration,
        )
        from prefect.orion.utilities.database import get_dialect

        dialect = get_dialect()

        if dialect.name == "postgresql":
            orm = AsyncPostgresORMConfiguration()
        elif dialect.name == "sqlite":
            orm = AioSqliteORMConfiguration()
        else:
            raise ValueError(
                f"Unable to infer orm configuration from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["orm"] = orm

    return OrionDBInterface(
        database_config=database_config,
        query_components=query_components,
        orm=orm,
    )


def inject_db(fn):
    """
    Decorator that provides a database interface to a function.

    The decorated function _must_ take a `db` kwarg and if a db is passed
    when called it will be used instead of creating a new one.

    If the function is a coroutine function, the wrapper will await the
    function's result. Otherwise, the wrapper will call the function
    normally.
    """

    def inject(kwargs):
        if "db" not in kwargs or kwargs["db"] is None:
            kwargs["db"] = provide_database_interface()

    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        inject(kwargs)
        return await fn(*args, **kwargs)

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        inject(kwargs)
        return fn(*args, **kwargs)

    if inspect.iscoroutinefunction(fn):
        return async_wrapper
    return sync_wrapper


@contextmanager
def temporary_database_config(tmp_database_config):
    starting_config = MODELS_DEPENDENCIES["database_config"]
    try:
        MODELS_DEPENDENCIES["database_config"] = tmp_database_config
        yield
    finally:
        MODELS_DEPENDENCIES["database_config"] = starting_config


@contextmanager
def temporary_query_components(tmp_queries):
    starting_queries = MODELS_DEPENDENCIES["query_components"]
    try:
        MODELS_DEPENDENCIES["query_components"] = tmp_queries
        yield
    finally:
        MODELS_DEPENDENCIES["query_components"] = starting_queries


@contextmanager
def temporary_orm_config(tmp_orm_config):
    starting_orm_config = MODELS_DEPENDENCIES["orm"]
    try:
        MODELS_DEPENDENCIES["orm"] = tmp_orm_config
        yield
    finally:
        MODELS_DEPENDENCIES["orm"] = starting_orm_config


def set_database_config(database_config):
    """Set Orion database configuration"""
    MODELS_DEPENDENCIES["database_config"] = database_config


def set_query_components(query_components):
    """Set Orion query components"""
    MODELS_DEPENDENCIES["query_components"] = query_components


def set_orm_config(orm_config):
    """Set Orion orm configuration"""
    MODELS_DEPENDENCIES["orm"] = orm_config
