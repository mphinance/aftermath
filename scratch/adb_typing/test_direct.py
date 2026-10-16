import subprocess

# Clear field: tap title, select all, delete
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'tap', '1500', '314'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '29', '--meta', '113'])
subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])
for _ in range(35):
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '67'])

# Try direct subprocess passing
test_str = "Testing: 123, didn't? Yes! ~Michael"
# In Android input text, space is %s
escaped = test_str.replace(" ", "%s")
res = subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'text', escaped], capture_output=True, text=True)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
