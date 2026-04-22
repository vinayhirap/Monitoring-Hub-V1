# app/db.py
import mysql.connector
from mysql.connector import pooling

_pool = pooling.MySQLConnectionPool(
    pool_name="monitoring_pool",
    pool_size=10,          # 10 simultaneous DB connections
    pool_reset_session=True,
    host="127.0.0.1",
    port=3307,
    user="root",
    password="root123",
    database="monitoring_hub",
    use_pure=True,
    connection_timeout=10,
)


def get_connection():
    return _pool.get_connection()