import boto3
import datetime

def fetch_metric(namespace, metric_name, statistic, resource_id, interval):
    print("CW RAW RESPONSE:", response)
    
    cw = boto3.client("cloudwatch")

    response = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {"Name": "InstanceId", "Value": resource_id}
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=5),
        EndTime=datetime.datetime.utcnow(),
        Period=interval,
        Statistics=[statistic]
    )

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return None

    return datapoints[-1][statistic]