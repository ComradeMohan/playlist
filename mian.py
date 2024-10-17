from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_playlist(playlist_url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'noplaylist': False,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

@app.post("/download/")
async def download(playlist_url: str = Form(...)):
    try:
        download_playlist(playlist_url)
        return {"status": "success", "message": "Playlist download started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def serve_html():
    with open("index.html", "r") as file:
        return file.read()
