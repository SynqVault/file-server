import os
import http.server
import socketserver
from urllib.parse import unquote
from html import escape

# CONFIG
PORT = 8888
DIRECTORY = "/opt/files/shared"  # Change this to your shared folder path

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>{folder} – SynqVault</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" />
    <style>
        body {{
            margin: 0;
            padding: 30px;
            font-family: 'Roboto', sans-serif;
            background-color: #121212;
            color: #e0e0e0;
        }}
        h1 {{
            font-size: 22px;
            font-weight: 500;
            color: #4da1ff;
            margin-bottom: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #1c1c1c;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.4);
        }}
        th, td {{
            padding: 14px 16px;
            border-bottom: 1px solid #2a2a2a;
            text-align: left;
            font-size: 14px;
        }}
        th {{
            background-color: #181818;
            color: #4da1ff;
            text-transform: uppercase;
            font-weight: 600;
            font-size: 12px;
        }}
        tr:hover td {{
            background-color: #2a2a2a;
        }}
        a {{
            color: #88ccff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #4da1ff;
        }}
        .folder {{
            color: #77ffcc;
            font-weight: 500;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>📂 {folder}</h1>
    <table>
        <tr><th>Name</th><th>Size</th></tr>
        {entries}
    </table>
    <div class="footer">
        <a href="https://discord.gg/your-invite" target="_blank">💬 Join the Discord</a>
    </div>
</body>
</html>
"""

class ThemedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def list_directory(self, path):
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        entries.sort(key=lambda a: a.lower())
        files_html = []

        # Add parent directory link if not root
        if self.path not in ["/", ""]:
            files_html.append(
                '<tr><td class="folder"><a href="..">⬅️ 📁 Parent Directory</a></td><td></td></tr>'
            )

        for name in entries:
            fullname = os.path.join(path, name)
            display_name = escape(name)
            link_name = escape(name)
            size = ""

            if os.path.isdir(fullname):
                display_name += "/"
                link_name += "/"
                size = "Folder"
                row = f'<tr><td class="folder"><a href="{link_name}">📁 {display_name}</a></td><td>{size}</td></tr>'
            else:
                size = self.format_size(os.path.getsize(fullname))
                row = f'<tr><td><a href="{link_name}">📄 {display_name}</a></td><td>{size}</td></tr>'

            files_html.append(row)

        folder_name = os.path.basename(os.path.normpath(path)) or "Root"
        response = HTML_TEMPLATE.format(
            folder=escape(folder_name),
            entries="\n".join(files_html),
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        return self.wfile.write(response)

    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

# Allow address reuse to prevent port locking
class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# Start the server
if __name__ == "__main__":
    try:
        with ReuseTCPServer(("0.0.0.0", PORT), ThemedHTTPRequestHandler) as httpd:
            print(f"🚀 SynqVault running at http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}")
