import yt_dlp

#paste your youtube video url
url = "https://youtu.be/cfB9E5tWk00?si=g3yiERyMeTEFVkNg"
ydl_opts = {
    "format": "best",
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    print(f"Title: {info['title']}")

#print download complete status
    print("Download complete!")
