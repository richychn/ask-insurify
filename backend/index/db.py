from sqlalchemy import create_engine, inspect
from local import PG_URL

def table_exists(table_name):
    engine = create_engine(PG_URL)
    exists = inspect(engine).has_table(f'data_{table_name}')
    engine.dispose()
    return exists