import urllib.request
import urllib.parse
import subprocess
import os
import time
import glob
import shutil

work_dir = "/tmp/narrated_demo"
os.makedirs(work_dir, exist_ok=True)
for f in glob.glob(f"{work_dir}/*"):
    os.remove(f)

# 8 Key Scenes with their narration script and app state
storyboard = [
    {
        "action": "street",
        "label": "1. Map Navigation",
        "script": "Welcome to FestiGuide, the AI-powered visual festival planner running natively on mobile."
    },
    {
        "action": "sat",
        "label": "2. Satellite Routing",
        "script": "Explore real festival grounds with high-resolution aerial satellite imagery and live stage routing."
    },
    {
        "action": "timeline",
        "label": "3. Timeline & Transit",
        "script": "Your personal schedule automatically optimizes set times, transit buffers, and rest stops."
    },
    {
        "action": "preview",
        "label": "4. Audio Preview",
        "script": "Tap any artist on your schedule to preview their top tracks directly in the floating audio player."
    },
    {
        "action": "swap",
        "label": "5. Alternative Lineup Swap",
        "script": "Need a change? Easily swap any act with real alternative artists performing that day."
    },
    {
        "action": "discovery",
        "label": "6. Discovery Recommendations",
        "script": "Discover hidden gem artists tailored precisely to your favorite genres and musical taste."
    },
    {
        "action": "profile",
        "label": "7. Memory & Preferences",
        "script": "FestiGuide remembers your walking pace, dietary preferences, and synced music memory across sessions."
    },
    {
        "action": "poster",
        "label": "8. Personalized Poster",
        "script": "And generate a custom personalized festival lineup poster ready to share with friends."
    }
]

print("1. Generating voiceover audio clips for each scene...")
audio_files = []
scene_durations = []

for idx, scene in enumerate(storyboard):
    print(f"  Generating voiceover {idx+1}/{len(storyboard)}: {scene['label']}...")
    text = scene["script"]
    encoded_text = urllib.parse.quote(text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl=en&client=tw-ob"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    mp3_path = f"{work_dir}/audio_{idx:02d}.mp3"
    with urllib.request.urlopen(req) as resp:
        with open(mp3_path, "wb") as f:
            f.write(resp.read())
            
    # Measure audio duration with ffprobe
    res = subprocess.run([
        "ffprobe", "-i", mp3_path,
        "-show_entries", "format=duration",
        "-v", "quiet", "-of", "csv=p=0"
    ], stdout=subprocess.PIPE, text=True, check=True)
    
    audio_dur = float(res.stdout.strip())
    # Add 0.5s padding so narration breathes
    total_dur = max(audio_dur + 0.6, 4.0)
    audio_files.append(mp3_path)
    scene_durations.append(total_dur)
    print(f"    Audio duration: {audio_dur:.2f}s -> Scene display duration: {total_dur:.2f}s")

print("\n2. Capturing visual frames for each scene...")
fps = 10
frame_num = 0

for idx, scene in enumerate(storyboard):
    dur = scene_durations[idx]
    print(f"  Rendering Scene {idx+1}: {scene['label']} ({dur:.1f}s)...")
    screenshot_path = f"{work_dir}/scene_{idx:02d}.png"
    
    # Take high-res headless screenshot of this exact state
    url = f"http://localhost:8000/?action={scene['action']}"
    subprocess.run([
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=2000",
        "--window-size=1080,950",
        f"--screenshot={screenshot_path}",
        url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    num_frames = int(dur * fps)
    for _ in range(num_frames):
        dest = f"{work_dir}/frame_{frame_num:05d}.png"
        shutil.copyfile(screenshot_path, dest)
        frame_num += 1

print("\n3. Concatenating audio voiceover track...")
# Build audio concat filter
concat_list_file = f"{work_dir}/audio_concat.txt"
with open(concat_list_file, "w") as f:
    for idx, (mp3, dur) in enumerate(zip(audio_files, scene_durations)):
        # Pad each audio file to match scene duration
        padded_mp3 = f"{work_dir}/padded_{idx:02d}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3,
            "-af", f"apad=whole_dur={dur}",
            padded_mp3
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        f.write(f"file '{padded_mp3}'\n")

combined_audio = f"{work_dir}/voiceover.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list_file,
    "-c:a", "pcm_s16le",
    combined_audio
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print("\n4. Encoding full video with synchronized voiceover...")
output_video = "/config/Desktop/BuildWithGemini/festiguide_demo.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", f"{work_dir}/frame_%05d.png",
    "-i", combined_audio,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    output_video
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

print("\n=== Voiceover Demo Video Created Successfully! ===")
print("File:", output_video)
