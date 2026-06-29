"""
Re-download ShareChat Claude data fresh from HuggingFace.
Source: tucnguyen/ShareChat

Run this to ensure the CSV is the original unmodified release.
Output: data/sharechat/claude_results_final_language_filtered.csv (overwritten)
"""

from huggingface_hub import hf_hub_download
import shutil
import os

REPO_ID   = "tucnguyen/ShareChat"
FILENAME  = "claude_results_final_language_filtered.csv"
OUT_PATH  = f"data/sharechat/{FILENAME}"

print(f"Downloading {FILENAME} from {REPO_ID} ...")
path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    repo_type="dataset",
    force_download=True,   # bypass cache, always fetch fresh
)
shutil.copy(path, OUT_PATH)
size = os.path.getsize(OUT_PATH)
print(f"Saved to {OUT_PATH}  ({size:,} bytes)")
