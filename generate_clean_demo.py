import subprocess
import os
import time
import glob
import shutil

frames_dir = "/tmp/clean_demo_frames"
os.makedirs(frames_dir, exist_ok=True)
for f in glob.glob(f"{frames_dir}/*"):
    os.remove(f)

# Define the storyboard for the 30-second demo:
# (action_param, duration_seconds, label)
scenes = [
    ("street", 4.0, "1. Interactive Map (Streets)"),
    ("sat", 4.0, "2. Satellite Aerial Routing"),
    ("timeline", 4.0, "3. Day Schedule & Walking Transit"),
    ("preview", 4.5, "4. Floating Music Player Preview"),
    ("swap", 4.5, "5. Alternative Lineup Swap Sheet"),
    ("discovery", 4.0, "6. Discovery Taste Recommendations"),
    ("profile", 4.0, "7. Memory Cloud & Walking Pace"),
    ("poster", 4.5, "8. Custom Festival Poster")
]

fps = 10
frame_num = 0

print("Generating demo scenes...")
for idx, (action, duration, label) in enumerate(scenes):
    print(f"Capturing Scene {idx+1}/{len(scenes)}: {label}...")
    screenshot_path = f"/tmp/scene_{idx}.png"
    
    # Take high-res headless screenshot of this exact state
    url = f"http://localhost:8000/?action={action}"
    subprocess.run([
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=2000",
        "--window-size=1080,950",
        f"--screenshot={screenshot_path}",
        url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Repeat the frame to cover duration at fps
    num_frames = int(duration * fps)
    for _ in range(num_frames):
        dest = f"{frames_dir}/frame_{frame_num:05d}.png"
        shutil.copyfile(screenshot_path, dest)
        frame_num += 1

print(f"Captured {frame_num} total frames. Encoding MP4 video...")
output_video = "/config/Desktop/BuildWithGemini/festiguide_demo.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", f"{frames_dir}/frame_%05d.png",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    output_video
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

print("Demo video created successfully!")
