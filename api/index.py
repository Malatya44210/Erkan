from http.server import BaseHTTPRequestHandler
import yt_dlp
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query).get('q', [''])[0]
        
        if not query:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Parametre eksik: ?q=sarki_adi")
            return

        try:
            ydl_opts = {'format': 'bestaudio', 'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                
                # Liste boş mu diye kontrol et (Hatanın sebebi buydu)
                entries = info.get('entries', [])
                if not entries:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Video bulunamadi")
                    return
                
                video_url = entries[0]['url']
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(video_url.encode())
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
