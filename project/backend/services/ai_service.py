import httpx
import hmac
import hashlib
from ..core.config import settings

CHATBASE_API_URL = "https://www.chatbase.co/api/v1/chat"

async def query_chatbase_assistant(question: str, user_id: int) -> dict:
    """
    Sends a question to the Chatbase API with a secure user hash.

    Args:
        question: The user's question.
        user_id: The unique ID of the user from our own database.

    Returns:
        A dictionary containing the AI's answer.
    """
    if not settings.CHATBASE_API_KEY or not settings.CHATBASE_SECRET_KEY:
        return {"answer": "AI service is not configured on the backend."}

    # --- Replicate the secure hashing logic in Python ---
    # The user ID must be a string for hashing
    user_id_str = str(user_id)
    secret_key_bytes = settings.CHATBASE_SECRET_KEY.encode('utf-8')
    user_id_bytes = user_id_str.encode('utf-8')
    
    # Create the HMAC-SHA256 hash
    user_id_hash = hmac.new(secret_key_bytes, user_id_bytes, hashlib.sha256).hexdigest()
    # --- End of hashing logic ---

    # Prepare the request headers
    headers = {
        "Authorization": f"Bearer {settings.CHATBASE_API_KEY}",
        "X-User-Id-Hash": user_id_hash,
        "Content-Type": "application/json"
    }

    # Prepare the request body
    data = {
        "messages": [
            {"content": question, "role": "user"}
        ],
        "stream": False,
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print(f"Sending query to Chatbase for user hash: {user_id_hash}")
            response = await client.post(CHATBASE_API_URL, json=data, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            # The answer is in the 'text' field of the response
            answer = response_data.get("text", "Sorry, I received a response but could not find an answer.")
            
            return {"answer": answer}
        
        except httpx.RequestError as e:
            print(f"Error connecting to Chatbase: {e}")
            return {"answer": "Sorry, I could not connect to the AI assistant service."}
        except httpx.HTTPStatusError as e:
            print(f"Chatbase returned an error: {e.response.status_code} - {e.response.text}")
            return {"answer": "The AI assistant service returned an error. Please check the backend logs."}