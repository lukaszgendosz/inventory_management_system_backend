from fastapi import APIRouter

router = APIRouter(tags=['Assets'])

@router.get('/assets')
def get_assets():
    pass
