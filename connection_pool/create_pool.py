"""
- SQLAlchemy automatically manages a connection pool for us.

- When call create_engine(), SQLAlchemy creates a connection pool automatically (unless explicitly tell it not to).
By default it uses QueuePool, which is a thread-safe pool that maintains a fixed number of database connections.
"""

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:12345@localhost:3306/alchemyDB",
    pool_size=20,          # base connections
    max_overflow=10,       # burst capacity
    pool_timeout=30,       # wait for 30s if pool exhausted
    pool_recycle=1800,     # recycle every 30min to avoid stale connections
    pool_pre_ping=True,    # check connection liveness
    echo=True
)
