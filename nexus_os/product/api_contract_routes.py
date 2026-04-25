from fastapi import APIRouter

router = APIRouter(prefix="/api/contracts", tags=["contracts"])


@router.get("/health")
def contract_health() -> dict:
    return {
        "ok": True,
        "status": "limited",
        "reason": "contract route module loaded; detailed market routes are not implemented in this baseline",
    }
