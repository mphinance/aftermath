import subprocess, time

# Clear body
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'tap', '1500', '350'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '29', '--meta', '113'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])
for _ in range(30):
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])

# Clear title
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'tap', '1500', '290'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '29', '--meta', '113'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])
for _ in range(40):
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])

