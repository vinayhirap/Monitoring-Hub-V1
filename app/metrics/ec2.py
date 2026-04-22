import random

def get_cpu_utilization(instance_id: str, region: str):
    return round(random.uniform(10, 95), 2)