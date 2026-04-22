def get_ec2_instances(region: str, environment: str):
    return [
        {
            "instance_id": "i-mock123",
            "name": "mock-ec2-1",
            "db_id": 1
        },
        {
            "instance_id": "i-mock456",
            "name": "mock-ec2-2",
            "db_id": 2
        }
    ]