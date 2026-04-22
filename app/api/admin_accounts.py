from fastapi import APIRouter, HTTPException
from app.db import get_connection
from app.aws.sts import test_assume_role

router = APIRouter(prefix="/admin/aws-accounts", tags=["Admin"])


@router.post("/")
def add_aws_account(payload: dict):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO aws_accounts
            (account_name, account_id, role_arn, external_id, default_region, status)
            VALUES (%s, %s, %s, %s, %s, 'active')
        """, (
            payload["account_name"],
            payload["account_id"],
            payload["role_arn"],
            payload["external_id"],
            payload["default_region"]
        ))

        conn.commit()
        return {"message": "AWS account added successfully"}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")

    except Exception as e:
        print("ADD ACCOUNT ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to add AWS account")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.post("/test-connection")
def test_connection(payload: dict):
    try:
        test_assume_role(
            role_arn=payload["role_arn"],
            external_id=payload["external_id"],
            region=payload["region"]
        )
        return {"status": "success"}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{account_id}/discover")
def trigger_discovery(account_id: int):
    try:
        from app.collector.discovery_ec2 import discover_ec2_for_account

        discover_ec2_for_account(account_id)
        return {"message": f"Discovery triggered for account {account_id}"}

    except Exception as e:
        print("DISCOVERY ERROR:", e)
        raise HTTPException(status_code=500, detail="Discovery failed")
