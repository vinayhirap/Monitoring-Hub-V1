# test_cw.py
import boto3
from datetime import datetime, timedelta

cw = boto3.client("cloudwatch", region_name="ap-south-1")

resp = cw.get_metric_statistics(
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[{"Name":"InstanceId","Value":"i-02b9635fb5da05fbb"}],
    StartTime=datetime.utcnow() - timedelta(minutes=15),
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=["Average"]
)

print(resp)