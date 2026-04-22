from datetime import datetime, timedelta
from app.db import get_connection
from app.aws.cloudwatch import fetch_metric
from app.collector.metrics_writer import write_metric

def collect_ec2_metrics():
    print("🔥 EC2 COLLECTOR STARTED 🔥")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, r.resource_id, a.default_region
        FROM resources r
        JOIN aws_accounts a ON r.account_id = a.id
        WHERE r.resource_type = 'ec2'
    """)
    instances = cursor.fetchall()

    for inst in instances:
        value = fetch_metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",   # ✅ FIXED
            dimensions=[{
                "Name": "InstanceId",
                "Value": inst["resource_id"]
            }],
            statistic="Average",
            period=300,
            region=inst["default_region"],
            start_time=datetime.utcnow() - timedelta(minutes=10),
            end_time=datetime.utcnow()
        )

        print("CW DEBUG =>", inst["resource_id"], value)

        if value is None:
            continue

        write_metric(
            resource_db_id=inst["id"],
            metric_name="cpuutilization",
            metric_value=value
        )

    cursor.close()
    conn.close()