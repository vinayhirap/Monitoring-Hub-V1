from fastapi import APIRouter, Query, HTTPException
from botocore.exceptions import BotoCoreError, ClientError
from app.aws.ec2 import get_ec2_instances
from app.metrics.ec2 import get_cpu_utilization
from app.health.evaluator import evaluate_cpu

router = APIRouter()

@router.get("/ec2")
def ec2_health(
    region: str = Query(...),
    environment: str = Query(...)
):
    try:
        instances = get_ec2_instances(region, environment)
        results = []

        for instance in instances:
            cpu = get_cpu_utilization(instance["instance_id"], region)
            health, severity = evaluate_cpu(cpu, environment)

            results.append({
                "instance_id": instance["instance_id"],
                "cpu": cpu,
                "health": health,
                "severity": severity,
                "ebs": [],
            })

        return {
            "region": region,
            "environment": environment,
            "count": len(results),
            "resources": results,
        }

    except (ClientError, BotoCoreError) as aws_err:
        raise HTTPException(
            status_code=502,
            detail=f"AWS error: {str(aws_err)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )