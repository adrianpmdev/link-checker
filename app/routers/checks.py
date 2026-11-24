"""
Checks router

Endpoint to run a link check on demand, without waiting for the scheduler.

@author adrianpmdev
"""

from fastapi import APIRouter, HTTPException, status

from app.checker import CheckAlreadyRunningError, check_all_products
from app.schemas import CheckSummary

router = APIRouter(prefix="/checks", tags=["Checks"])


@router.post("/run", response_model=CheckSummary)
def run_check():
    """Check every product link now. Answers 409 if a check is already running."""
    try:
        return check_all_products()
    except CheckAlreadyRunningError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A link check is already running"
        ) from error
