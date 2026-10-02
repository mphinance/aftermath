import subprocess, time

def send_token(token):
    # If token is newline
    if token == '\n':
        subprocess.run(['adb', '-s', 'arc:5555', 'shell', 'input', 'keyevent', '66'])
        return
    # Replace space with %s
    token = token.replace(' ', '%s')
    # Escapes for adb shell
    for char in ['"', "'", '(', ')', '&', '<', '>', ';', '*', '|', '~', '$']:
        token = token.replace(char, f'\\{char}')
    subprocess.run(['adb', '-s', 'arc:5555', 'shell', f'input text "{token}"'])

print("Testing send_token...")
