# app/health/evaluator.py

from app.db import get_connection
from app.config import RULES  # assuming RULES is loaded here


def get_threshold_from_db(metric_name: str, resource_type: str):
    """
    Fetch threshold values from DB for a given metric and resource type.
    Returns dict with warning_value and critical_value or None.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT
            t.warning_value,
            t.critical_value
        FROM thresholds t
        JOIN metric_catalog mc ON mc.id = t.metric_id
        WHERE mc.metric_name = %s
          AND t.resource_type = %s
          AND t.enabled = 1
        LIMIT 1
        """,
        (metric_name, resource_type),
    )

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def evaluate_cpu(cpu_value: float, environment: str):
    """
    Evaluate CPU health.
    Priority:
    1. DB thresholds
    2. YAML thresholds (fallback)

    Returns:
        (health_color, severity_level)
    """

    # 1️⃣ Try DB thresholds
    db_threshold = get_threshold_from_db("cpputilization", "ec2")

    if db_threshold:
        warning = db_threshold["warning_value"]
        critical = db_threshold["critical_value"]
    else:
        # 2️⃣ YAML fallback (existing behavior)
        thresholds = RULES["severity"][environment]["cpu"]
        warning = thresholds["warning"]
        critical = thresholds["critical"]

    # 3️⃣ Health evaluation
    if cpu_value >= critical:
        return "red", 2
    elif cpu_value >= warning:
        return "amber", 1
    else:
        return "green", 0
