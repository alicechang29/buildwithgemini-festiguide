#!/bin/bash
set -e

OUTPUT="/config/Desktop/BuildWithGemini/festiguide_demo.mp4"
DURATION=30

echo "=== FestiGuide Automated Demo Recorder ==="
echo "Target output: $OUTPUT"

# Launch browser to tour URL
/config/automata/bin/xdg-open "http://localhost:8000/?tour=1"
sleep 2

# Maximize or focus Chrome window if possible
WINDOW_ID=$(xdotool search --onlyvisible --class "google-chrome" | head -n 1 || true)
if [ -n "$WINDOW_ID" ]; then
    xdotool windowactivate "$WINDOW_ID" || true
fi

echo "Recording screen for $DURATION seconds with ffmpeg..."
# Record screen around the center or full display
ffmpeg -y \
  -f x11grab \
  -video_size 1920x1080 \
  -framerate 30 \
  -i "$DISPLAY+534,189" \
  -c:v libx264 \
  -preset fast \
  -crf 22 \
  -pix_fmt yuv420p \
  -t "$DURATION" \
  "$OUTPUT"

echo "=== Recording Complete! File saved to: $OUTPUT ==="
ls -lh "$OUTPUT"
