import subprocess
import time
import sys
import logging
from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("type_part2.log", mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)

DEVICE = "arc:5555"

def adb_run(cmd_str):
    res = subprocess.run(["adb", "-s", DEVICE, "shell", cmd_str], capture_output=True, text=True)
    if res.returncode != 0:
        logging.warning(f"ADB warning: {res.stderr.strip()}")
    return res

def text_to_adb_cmds(text):
    cmds = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '\n':
            cmds.append("input keyevent 66")
            i += 1
        elif ch == ' ':
            cmds.append("input text %s")
            i += 1
        elif ch in ("'", "’"):
            cmds.append("input keyevent 75")
            i += 1
        elif ch == '~':
            cmds.append("input text '~'")
            i += 1
        elif ch == '%':
            cmds.append("input text '%'")
            i += 1
        elif ch in ('"', '`'):
            cmds.append("input keyevent 75 --meta 1")
            i += 1
        else:
            j = i
            while j < len(text) and text[j] not in ('\n', ' ', "'", "’", '~', '%', '"', '`'):
                j += 1
            chunk = text[i:j]
            cmds.append(f"input text '{chunk}'")
            i = j
    return cmds

def type_string(text, label="Text", batch_size=8, delay=0.03):
    logging.info(f"Starting to type {label} ({len(text)} characters)...")
    cmds = text_to_adb_cmds(text)
    total = len(cmds)
    for idx in range(0, total, batch_size):
        batch = cmds[idx:idx+batch_size]
        full_cmd = "; ".join(batch)
        adb_run(full_cmd)
        progress = min(100, int((idx + len(batch)) / total * 100))
        logging.info(f"Typing {label}: {progress}% complete")
        time.sleep(delay)
    logging.info(f"Finished typing {label} successfully.")

BODY_PART2 = """

HERE IS A LIVE TEST ON $NVDA:

I just ran 3 of these tools against $NVDA (Spot: $218.29):

1. get_apex_levels: The Gamma Flip sits at $209.97. Spot is above the flip, meaning dealers are long gamma and absorbing volatility. The dominant overhead magnet is the $230 strike (Score 100, 133k OI, +$95.8M GEX). The structural floor sits at $210 (116k OI).

2. get_iv_rank: IV Rank is 0.9 out of 100. Volatility is pinned at the literal floor of its 52-week band. Option premium is dirt cheap. Selling Cash-Secured Puts here offers poor risk-reward; buying premium or calendar structures is favored.

3. get_dark_pool: Over the last 5 days, 276 off-exchange prints crossed for $1.04B notional, leaning distribution (-$594M net notional). Large desks are patiently trimming size into the rally.

An LLM with no tools guesses. An LLM with MCP reads the actual tape.

Stop trading off vibes."""

def main():
    logging.info("=== Appending Part 2 ($NVDA Live Results) ===")
    type_string(BODY_PART2, label="Body Part 2", batch_size=7, delay=0.03)
    time.sleep(1.5)
    
    # Save verification crop
    subprocess.run(["adb", "-s", DEVICE, "exec-out", "screencap", "-p"], stdout=open("/tmp/part2_result.png", "wb"))
    im = Image.open("/tmp/part2_result.png")
    crop = im.crop((1410, 173, 1909, 1000))
    crop.save("/tmp/part2_crop.png")
    logging.info("Saved verification crop to /tmp/part2_crop.png")
    logging.info("=== Complete. Post button untouched. ===")

if __name__ == "__main__":
    main()
