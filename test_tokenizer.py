import re

def tokenize(text):
    tokens = []
    # Match words, spaces, newlines, or specific symbols
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '\n':
            tokens.append(('KEY', 66))
            i += 1
        elif ch == ' ':
            tokens.append(('TEXT', '%s'))
            i += 1
        elif ch in ("'", "’"):
            tokens.append(('KEY', 75))
            i += 1
        elif ch == '~':
            tokens.append(('TEXT', '\\~'))
            i += 1
        elif ch == '%':
            tokens.append(('TEXT', '\\%'))
            i += 1
        else:
            # Consume run of alphanumeric + standard punctuation
            j = i
            while j < len(text) and text[j] not in ('\n', ' ', "'", "’", '~', '%'):
                j += 1
            tokens.append(('TEXT', text[i:j]))
            i = j
    return tokens

sample = "I AM MPHINCIAL AI. Michael didn’t write this. 52.5% ~ Michael"
tokens = tokenize(sample)
print("Tokens count:", len(tokens))
for t in tokens[:10]:
    print(t)
