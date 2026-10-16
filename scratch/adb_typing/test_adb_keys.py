import subprocess

def test_key():
    # Tap body
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'tap', '1500', '350'])
    # Try percent
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'text', '52.5\\%'])
    # Try enter
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '66'])
    # Try apostrophe
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'text', 'didn'])
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '75'])
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'text', 't'])

test_key()
