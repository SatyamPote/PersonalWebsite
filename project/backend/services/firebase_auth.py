import firebase_admin
from firebase_admin import credentials, auth
import base64
import json
from core.config import settings

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK if it hasn't been already.
    It decodes the Base64 service account key from settings.
    """
    if not firebase_admin._apps:
        try:
            # Decode the base64 string to bytes
            decoded_service_account_bytes = base64.b64decode(settings.FIREBASE_SERVICE_ACCOUNT_JSON_BASE64)
            
            # Convert bytes to a dictionary
            service_account_info = json.loads(decoded_service_account_bytes.decode('utf-8'))
            
            # Initialize the app
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized successfully.")
        except Exception as e:
            print(f"❌ FAILED TO INITIALIZE FIREBASE: {e}")
            # Depending on your app's needs, you might want to raise the exception
            # to prevent the app from starting without Firebase.
            raise

def verify_id_token(id_token: str) -> dict:
    """
    Verifies the Firebase ID token and returns the decoded user claims.
    
    Args:
        id_token: The Firebase ID token sent from the client.

    Returns:
        A dictionary containing the user's decoded information (uid, email, etc.).
        
    Raises:
        ValueError: If the token is invalid or expired.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        raise ValueError("Invalid or expired Firebase ID token.")