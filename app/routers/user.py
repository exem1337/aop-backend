from fastapi import APIRouter

router = APIRouter()

@router.get('/me')
def getCurrentUser():
  return { "id": 0, "lastname": 'sasa' }