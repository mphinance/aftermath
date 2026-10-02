import re, subprocess

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
            cmds.append("input text '\\~'")
            i += 1
        elif ch == '%':
            cmds.append("input text '\\%'")
            i += 1
        else:
            j = i
            while j < len(text) and text[j] not in ('\n', ' ', "'", "’", '~', '%'):
                j += 1
            chunk = text[i:j]
            cmds.append(f"input text '{chunk}'")
            i = j
    return cmds

text = "I AM MPHINCIAL AI. Michael didn't write this. 52.5% ~ Michael"
cmds = text_to_adb_cmds(text)
full_cmd = "; ".join(cmds)
print("Command length:", len(full_cmd))
print("Sample:", full_cmd[:100])
