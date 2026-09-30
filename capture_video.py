import urllib.request
import json
import base64
import time
import os
import websocket
import subprocess

# Query the open page
req = urllib.request.urlopen("http://127.0.0.1:9222/json")
targets = json.loads(req.read().decode())
page_target = next(t for t in targets if t.get("type") == "page")
ws_url = page_target["webSocketDebuggerUrl"]

ws = websocket.create_connection(ws_url)

def send_cmd(method, params=None):
    cmd_id = int(time.time() * 1000) % 1000000
    msg = {"id": cmd_id, "method": method, "params": params or {}}
    ws.send(json.dumps(msg))
    while True:
        res = json.loads(ws.recv())
        if res.get("id") == cmd_id:
            return res.get("result", {})

print("Triggering demo tour in page...")
send_cmd("Runtime.evaluate", {"expression": "if (window.runDemoTour) window.runDemoTour();"})

frames_dir = "/tmp/demo_frames"
os.makedirs(frames_dir, exist_ok=True)

print("Capturing 60 high-res frames over 30 seconds (2 FPS)...")
start_time = time.time()
frame_count = 0

for i in range(75):
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    if "data" in res:
        data = base64.b64decode(res["data"])
        with open(f"{frames_dir}/frame_{i:04d}.png", "wb") as f:
            f.write(data)
        frame_count += 1
    time.sleep(0.4)

ws.close()
print(f"Captured {frame_count} frames. Encoding into MP4 with ffmpeg...")

output_video = "/config/Desktop/BuildWithGemini/festiguide_demo.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", "2.5",
    "-i", f"{frames_dir}/frame_%04d.png",
    "-c:v", "libx264",
    "-r", "30",
    "-pix_fmt", "yuv420p",
    output_video
], check=True)

print("Demo video created successfully at:", output_video)
