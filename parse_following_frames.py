#!/usr/bin/env python3
import os
import glob
import subprocess
import re
import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRAMES_DIR = str(BASE_DIR / "recordings" / "following_session")
OUTPUT_FILE = str(BASE_DIR / "data" / "following" / "following_usernames.txt")

frames = sorted(glob.glob(f"{FRAMES_DIR}/*.png"))
print(f"[*] Processing {len(frames)} frames for following usernames...")

raw_names = set()

for idx, fpath in enumerate(frames):
    img = cv2.imread(fpath)
    if img is None:
        continue
    
    # Crop username column
    # Y from 140 to 830 (exclude header and bottom nav)
    # X from 75 to 370 (exclude avatars on left and Following buttons on right)
    h, w = img.shape[:2]
    crop = img[135:min(835, h), 75:min(370, w)]
    
    temp_crop = "/tmp/temp_crop.png"
    cv2.imwrite(temp_crop, crop)
    
    try:
        out = subprocess.check_output(
            ["tesseract", temp_crop, "stdout", "--psm", "6", "-c", "tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ "],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
        
        lines = out.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Remove badges or noise
            # Split tokens if needed or take valid username strings
            tokens = line.split()
            for token in tokens:
                token = token.strip()
                # Usernames are typically 3 to 25 chars, alphanumeric or underscores
                if 3 <= len(token) <= 30 and re.match(r"^[A-Za-z0-9_]+$", token):
                    lower = token.lower()
                    if lower not in ["following", "followers", "mphinance", "market", "open", "for", "you", "chats"]:
                        raw_names.add(token)
    except Exception as e:
        pass

    if (idx + 1) % 25 == 0 or idx == len(frames) - 1:
        print(f"[*] Processed {idx + 1}/{len(frames)} frames... Found {len(raw_names)} candidate usernames so far.")

# Sort and save
sorted_names = sorted(list(raw_names), key=lambda s: s.lower())
with open(OUTPUT_FILE, "w") as f:
    for name in sorted_names:
        f.write(name + "\n")

print(f"\n[+] Total unique candidate usernames extracted: {len(sorted_names)}")
print(f"[+] Saved to: {OUTPUT_FILE}")
