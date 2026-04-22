# app/aws/cloudwatch.py

import boto3
from datetime import datetime, timedelta


def fetch_metric(
    namespace: str,
    metric_name: str,
    dimensions: list,
    statistic: str = "Average",
    period: int = 300,
    minutes: int = 5,
    region: str = "ap-south-2",
):
    """
    Generic CloudWatch metric fetcher
    Used by EC2, RDS, ALB, API Gateway, etc.
    """

    cw = boto3.client("cloudwatch", region_name=region)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    response = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
    )

    print("CW RAW RESPONSE:", response)

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return None

    latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
    return latest.get(statistic)