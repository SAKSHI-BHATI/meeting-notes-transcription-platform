from fastapi import HTTPException


def not_found(error: LookupError):
    raise HTTPException(status_code=404, detail={"code": "not_found", "message": str(error)})
