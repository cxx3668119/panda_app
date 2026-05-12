from sqlalchemy import inspect, text

from app import models  # noqa: F401
from app.db.base import Base
from app.db.engine import engine


def _quote_name(name: str) -> str:
    return f'`{name}`'


def _compile_column_type(column) -> str:
    return column.type.compile(dialect=engine.dialect)


def _ensure_missing_columns() -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue

            existing_columns = {
                column['name']
                for column in inspector.get_columns(table.name)
            }

            for column in table.columns:
                if column.primary_key or column.name in existing_columns:
                    continue

                column_type = _compile_column_type(column)
                statement = (
                    f'ALTER TABLE {_quote_name(table.name)} '
                    f'ADD COLUMN {_quote_name(column.name)} {column_type} NULL'
                )
                connection.execute(text(statement))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_missing_columns()


if __name__ == '__main__':
    init_db()
