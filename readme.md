# 🔐 Minimal File Server

Simple, clean, and fast — a Python-powered file server with a dark theme inspired by rclone’s index UI.

📁 Browse your files from any browser  
🌙 Dark mode, mobile-friendly  
⚡ Just Python – no dependencies

---

## ✅ Features

- Beautiful dark theme with folder/file icons
- “💬 Join Our Discord” footer link
- Automatic file size formatting (KB / MB / GB)
- Works on Windows, Linux, and macOS

---

## 🖥️ Requirements

- Python 3.x (pre-installed on most systems)

---

## 🚀 Quick Start

1. 📦 Clone this repo or download the script:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. 🛠 Edit your shared folder path:

Open file_server.py and change this line:

```python
DIRECTORY = r"/your/folder/path"
```

3. ▶️ Run the server:

```bash
python3 file_server.py
```

4. 🌐 Access in browser:

By default, the server listens on:

```
0.0.0.0:8888
```

That means you need to open your local IP address in your browser.  
To find your IP:

```bash
ip addr show   # Linux
ipconfig       # Windows
```

Then visit:

```
http://<your-ip>:8888
```

Example:

```
http://192.168.1.42:8888
```

---

## 🧠 Run in background (Linux/macOS)

With tmux:

```bash
tmux new -s fileserver
python3 file_server.py
# Press Ctrl+B then D to detach
```

With screen:

```bash
screen -S fileserver
python3 file_server.py
# Press Ctrl+A then D to detach
```

---

## 💬 Join Our Discord

👉 https://discord.gg/H6hvSmaDDs

---

## 📄 License

MIT License
