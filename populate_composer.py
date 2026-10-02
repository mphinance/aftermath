import subprocess
import time
import sys

DEVICE = "arc:5555"

TITLE = "The Clout Inversion: What 395 verified portfolios say about who actually has capital"

BODY_TEXT = """I ran an audit across 395 verified brokerage accounts connected to this app.

Not self-reported screenshots. Live Plaid-verified balances totaling $169,001,648 in tracked equity.

The math shows a massive disconnect between follower counts and actual capital on the tape:

1. The loudest accounts are rarely the largest:
Sir Jack has 231,000 followers and $12.2M verified. Respect to the founder, but that is $53 of capital per follower. Mostly parked in QQQ, SPY, and SGOV.

2. The actual heavyweights are nearly invisible:
- @SlowmoInvestor: $16.14M verified (28k AAPL, 20k NVDA). Only 1,846 followers. That is $8,747 per follower.
- @Trescommas: $15.05M verified (AAPL, ANET, NVDA). Only 2,261 followers. $6,659 per follower.
- @CptNut: $5.27M verified (heavy COIN). Only 423 followers. $12,471 per follower.
- @OCmd: $3.98M verified (MU, SPY, QQQ). Only 654 followers. $6,095 per follower.
- @NOLA: $3.77M verified (LLY). Only 187 followers. $20,169 per follower.
- @skrt: $2.39M verified (SPMO). Only 18 followers. That is $132,895 per follower.
- @engineered: $2.10M verified (META, VOO, GOOG). Only 35 followers. $60,119 per follower.
- @AnalysisPilot: $1.88M verified (VOO, SCHG). Only 6 followers. $314,527 per follower.
- @BearHugger: $1.45M verified (BAC). Exactly 2 followers. $729,107 per follower.

Out of 395 public connected traders, there are 31 verified millionaires controlling $110.78M.

Over 70% of that millionaire capital is sitting in accounts with under 2,000 followers.

If you are trying to learn how real money positions, stop tracking follower counts and start tracking verified tape.

I put together an open-source terminal tracking all 395 whales, their exact lot sizes, cost basis, and positioning:
github.com/mphinance/aftermath

~ Michael"""

def tap(x, y):
    subprocess.run(["adb", "-s", DEVICE, "shell", "input", "tap", str(x), str(y)])

def send_token(token):
    if token == '\n':
        subprocess.run(["adb", "-s", DEVICE, "shell", "input", "keyevent", "66"])
    elif token == ' ':
        subprocess.run(["adb", "-s", DEVICE, "shell", "input", "keyevent", "62"])
    elif token == '~':
        subprocess.run(["adb", "-s", DEVICE, "shell", "input", "text", "'~'"])
    else:
        escaped = token.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace("'", "\\'")
        subprocess.run(["adb", "-s", DEVICE, "shell", f"input text \"{escaped}\""])

def run():
    print("[*] Tapping Title field...")
    tap(1500, 330)
    time.sleep(0.5)
    
    # Type Title
    for word in TITLE.split(" "):
        escaped = word.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace("'", "\\'")
        subprocess.run(["adb", "-s", DEVICE, "shell", f"input text \"{escaped}\""])
        subprocess.run(["adb", "-s", DEVICE, "shell", "input", "keyevent", "62"])
        time.sleep(0.02)
    
    time.sleep(0.5)
    print("[*] Tapping Body field...")
    tap(1500, 520)
    time.sleep(0.5)
    
    # Type Body
    total = len(BODY_TEXT)
    i = 0
    while i < total:
        ch = BODY_TEXT[i]
        if ch == '\n':
            send_token('\n')
            i += 1
            time.sleep(0.04)
        elif ch == ' ':
            send_token(' ')
            i += 1
            time.sleep(0.02)
        elif ch == '~':
            send_token('~')
            i += 1
            time.sleep(0.02)
        else:
            j = i
            while j < total and BODY_TEXT[j] not in ('\n', ' ', '~'):
                j += 1
            word = BODY_TEXT[i:j]
            send_token(word)
            i = j
            time.sleep(0.02)
            
    print("[+] Done typing draft. POST BUTTON UNTOUCHED.")

if __name__ == "__main__":
    run()
