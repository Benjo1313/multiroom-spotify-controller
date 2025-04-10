from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import base64
import os
from typing import List, Optional, Dict, Any
import time
from urllib.parse import urlencode
from pydantic import BaseModel
import logging
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into os.environ

# Set up logging``
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Spotify Zone Control API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration - replace with your actual values from Spotify Developer Dashboard
#SPOTIFY_CLIENT_ID = "4fa396538b1649a2a7d8c41e453e009a"
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
logger.info(SPOTIFY_CLIENT_ID)
SPOTIFY_CLIENT_SECRET = "0746c66c01054425bb4a579d722db6fe"
REDIRECT_URI = "http://localhost:8000/callback"
API_BASE_URL = "https://api.spotify.com/v1"

# In-memory token storage (replace with database in production)
token_info = {
    "access_token": None,
    "refresh_token": None,
    "expires_at": 0
}

# Pydantic Models
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str

class SpotifyError(BaseModel):
    error: str
    error_description: str

# Helper functions
def get_auth_header():
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {auth_header}"}

def check_token():
    """Check if token exists and is valid, refresh if necessary"""
    global token_info
    
    if not token_info["access_token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated with Spotify"
        )
    
    # If token is expired, refresh it
    if token_info["expires_at"] < time.time():
        refresh_token()
    
    return {"Authorization": f"Bearer {token_info['access_token']}"}

async def refresh_token():
    """Refresh the access token using refresh token"""
    global token_info
    
    if not token_info["refresh_token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token available"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                headers=get_auth_header(),
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": token_info["refresh_token"]
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to refresh token: {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to refresh token"
                )
            
            token_data = response.json()
            token_info["access_token"] = token_data["access_token"]
            token_info["expires_at"] = time.time() + token_data["expires_in"]
            # Only update refresh_token if a new one is provided
            if "refresh_token" in token_data:
                token_info["refresh_token"] = token_data["refresh_token"]
                
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refreshing token: {str(e)}"
        )

# Routes
@app.get("/")
def read_root():
    return {"message": "Spotify Zone Control API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/login")
def login():
    """Initiate Spotify OAuth flow"""
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    print(SPOTIFY_CLIENT_ID)
    params = {
        "response_type": 'code',
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True
    }
    
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(code: str = None, error: str = None):
    """Handle Spotify OAuth callback"""
    if error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": error}
        )
    
    if not code:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Authorization code not provided"}
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                headers=get_auth_header(),
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Token exchange failed: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to exchange authorization code for token"}
                )
            
            token_data = response.json()
            global token_info
            token_info["access_token"] = token_data["access_token"]
            token_info["refresh_token"] = token_data["refresh_token"]
            token_info["expires_at"] = time.time() + token_data["expires_in"]
            
            # Redirect to frontend with success message
            return RedirectResponse(url="http://localhost:3000?auth=success")
            
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Error processing callback: {str(e)}"}
        )

@app.get("/api/spotify/now-playing")
async def get_now_playing():
    """Get information about the user's current playback state"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/me/player",
                headers=headers
            )
            
            if response.status_code == 204:
                return {"is_playing": False, "item": None}
            
            if response.status_code != 200:
                logger.error(f"Error getting playback state: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to get playback state"}
                )
            
            return response.json()
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting playback state: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting playback state: {str(e)}"
        )

@app.get("/api/spotify/devices")
async def get_devices():
    """Get information about the user's available devices"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/me/player/devices",
                headers=headers
            )
            
            if response.status_code != 200:
                logger.error(f"Error getting devices: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to get devices"}
                )
            
            return response.json()
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting devices: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting devices: {str(e)}"
        )

@app.post("/api/spotify/play")
async def play(device_id: Optional[str] = None):
    """Start/resume playback on the specified device"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            params = {}
            if device_id:
                params["device_id"] = device_id
                
            response = await client.put(
                f"{API_BASE_URL}/me/player/play",
                headers=headers,
                params=params
            )
            
            if response.status_code not in [200, 204]:
                logger.error(f"Error starting playback: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to start playback"}
                )
            
            return {"success": True}
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error starting playback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting playback: {str(e)}"
        )

@app.post("/api/spotify/pause")
async def pause(device_id: Optional[str] = None):
    """Pause playback on the specified device"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            params = {}
            if device_id:
                params["device_id"] = device_id
                
            response = await client.put(
                f"{API_BASE_URL}/me/player/pause",
                headers=headers,
                params=params
            )
            
            if response.status_code not in [200, 204]:
                logger.error(f"Error pausing playback: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to pause playback"}
                )
            
            return {"success": True}
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error pausing playback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error pausing playback: {str(e)}"
        )

@app.post("/api/spotify/next")
async def next_track(device_id: Optional[str] = None):
    """Skip to the next track"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            params = {}
            if device_id:
                params["device_id"] = device_id
                
            response = await client.post(
                f"{API_BASE_URL}/me/player/next",
                headers=headers,
                params=params
            )
            
            if response.status_code not in [200, 204]:
                logger.error(f"Error skipping to next track: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to skip to next track"}
                )
            
            return {"success": True}
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error skipping to next track: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error skipping to next track: {str(e)}"
        )

@app.post("/api/spotify/previous")
async def previous_track(device_id: Optional[str] = None):
    """Skip to the previous track"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            params = {}
            if device_id:
                params["device_id"] = device_id
                
            response = await client.post(
                f"{API_BASE_URL}/me/player/previous",
                headers=headers,
                params=params
            )
            
            if response.status_code not in [200, 204]:
                logger.error(f"Error skipping to previous track: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to skip to previous track"}
                )
            
            return {"success": True}
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error skipping to previous track: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error skipping to previous track: {str(e)}"
        )

@app.get("/api/spotify/queue")
async def get_queue():
    """Get user's queue"""
    try:
        headers = check_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/me/player/queue",
                headers=headers
            )
            
            if response.status_code != 200:
                logger.error(f"Error getting queue: {response.text}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": "Failed to get queue"}
                )
            
            return response.json()
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting queue: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)