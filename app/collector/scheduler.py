# app/collector/scheduler.py

from app.collector.ec2_cpu_collector import collect_ec2_metrics
from app.collector.alert_evaluator import evaluate_alerts

def run():
    print("Running EC2 EC2 metrics collector...")
    collect_ec2_metrics()

    print("Evaluating alerts (DB-driven)...")
    evaluate_alerts()

if __name__ == "__main__":
    run()