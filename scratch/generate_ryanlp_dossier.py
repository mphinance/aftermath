import os
import sys

dossier_path = "/home/mpha/artemis/afterhour/reports/dossiers/@RyanLP_quant_profile.md"

# Verify path can be opened
with open(dossier_path, "w", encoding="utf-8") as f:
    f.write("# Temporary stub\n")

print("File created successfully. Ready for full write.")
