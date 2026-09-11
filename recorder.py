#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import cv2
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = str(BASE_DIR / "recordings" / "following_session")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# App window crop bounds (x=1395, y=108, w=515, h=903)
X, Y, W, H = 1390, 100, 525, 915

prev_frame = None
frame_count = 0
saved_count = 0
max_duration_sec = 180
start_time = time.time()

print(f"[*] Starting feed recorder... Destination: {OUTPUT_DIR}")
print("[*] Ready! Scroll away at your own pace.")
sys.stdout.flush()

try:
    while (time.time() - start_time) < max_duration_sec:
        if os.path.exists("/tmp/stop_recording"):
            print("[*] Stop signal received.")
            break

        proc = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            capture_output=True,
            timeout=5
        )
        if proc.returncode != 0 or not proc.stdout:
            time.sleep(0.3)
            continue

        frame_count += 1
        img_array = np.frombuffer(proc.stdout, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            time.sleep(0.2)
            continue

        h_img, w_img = img.shape[:2]
        crop_y1 = min(max(0, Y), h_img)
        crop_y2 = min(max(0, Y + H), h_img)
        crop_x1 = min(max(0, X), w_img)
        crop_x2 = min(max(0, X + W), w_img)

        cropped = img[crop_y1:crop_y2, crop_x1:crop_x2]

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            score = np.mean(diff)
            if score < 1.5:
                time.sleep(0.4)
                continue

        prev_frame = gray
        saved_count += 1
        filename = os.path.join(OUTPUT_DIR, f"frame_{saved_count:04d}.png")
        cv2.imwrite(filename, cropped)
        print(f"[+] Captured frame #{saved_count} (total checks: {frame_count})")
        sys.stdout.flush()

        time.sleep(0.4)

except KeyboardInterrupt:
    print("\n[*] Stopped by user interrupt.")
except Exception as e:
    print(f"\n[!] Error during recording: {e}")

print(f"[*] Done! Captured {saved_count} unique frames in {OUTPUT_DIR}")
