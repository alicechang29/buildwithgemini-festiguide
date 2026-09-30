import subprocess
import time
import os
import glob
from PIL import Image

output_dir = "/tmp/demo_frames"
os.makedirs(output_dir, exist_ok=True)
for f in glob.glob(f"{output_dir}/*"):
    os.remove(f)

# The tour actions:
# 1. Map screen (street)
# 2. Map screen (sat)
# 3. Timeline
# 4. Swap modal
# 5. Discovery
# 6. Profile
# 7. Poster

steps = [
    # (screen, actions_js, duration_frames, label)
    ("map", "switchMapLayer('street');", 6, "Map Streets"),
    ("map", "switchMapLayer('satellite');", 6, "Map Satellite"),
    ("timeline", "switchScreen('timeline');", 8, "Timeline Sets"),
    ("timeline", "playAudioPreview('Anderson .Paak');", 6, "Audio Preview"),
    ("swap", "openSwapModal(0, 'Anderson .Paak');", 6, "Swap Alternative Act"),
    ("discovery", "closeSwapModal(); switchScreen('discovery');", 6, "Discovery Gems"),
    ("profile", "switchScreen('profile');", 6, "Memory & Preferences"),
    ("poster", "showPoster();", 8, "Personalized Lineup Poster"),
    ("map", "hidePoster(); switchScreen('map');", 6, "Back to Map")
]

frame_idx = 0
for step_idx, (screen, js_code, num_frames, label) in enumerate(steps):
    print(f"Step {step_idx+1}/{len(steps)}: {label}...")
    screenshot_path = f"/tmp/step_{step_idx}.png"
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--window-size=1200,980",
        f"--screenshot={screenshot_path}",
        f"http://localhost:8000/?step_js={js_code}"
    ]
    # We can pass script to execute or inject via a query param / HTML
    # Alternatively we can capture directly!
