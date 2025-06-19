from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services import ai_service
from ..db import models
from ..dependencies import get_current_user

router = APIRouter()

class AIQuery(BaseModel):
    question: str

@router.post("/query", summary="Query the Chatbase AI Assistant")
async def handle_ai_query(
    query: AIQuery,
    current_user: models.User = Depends(get_current_user)
):
    """
    Receives a question from the frontend, gets the current user's ID,
    and calls the Chatbase service with that information.
    """
    print(f"User {current_user.email} (ID: {current_user.id}) is asking: '{query.question}'")
    
    # Call our new Chatbase service with the question and the user's database ID
    response = await ai_service.query_chatbase_assistant(query.question, current_user.id)
    
    return response