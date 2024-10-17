from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import yt_dlp
import os

app = FastAPI()

# CORS Middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_playlist(playlist_url: str, cookies_file: str = None):
    """Download a YouTube playlist using yt-dlp."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',  # Output template for downloaded files
        'noplaylist': False,
        'cookiefile': cookies_file,  # Use a cookie file if needed
        'sleep_interval': 5,  # Sleep for 5 seconds between downloads to avoid rate limiting
        'postprocessors': [{  # Optional: Convert videos to mp3 after downloading
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

@app.post("/download/")
async def download(playlist_url: str = Form(...), cookies_file: str = Form(None)):
    """Endpoint to download a YouTube playlist."""
    try:
        download_playlist(playlist_url, cookies_file)
        return {"status": "success", "message": "Playlist download started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    """Serve the HTML page for the frontend."""
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)