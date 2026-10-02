import subprocess, shlex

def send_text(s):
    # adb shell input text handles many characters if properly quoted
    # Spaces must be %s
    escaped = s.replace(' ', '%s')
    # Use shlex.quote for shell safety
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'text', escaped])

send_text("I AM MPHINCIAL AI.")
