#!/bin/bash
#SBATCH --job-name=backend_chatbot
#SBATCH --partition=allgroups
#SBATCH --gres=gpu:rtx:1
#SBATCH --mem=24G            # un pic mai mult RAM
#SBATCH --time=24:00:00
#SBATCH --output=backend_%j.log
#SBATCH --error=backend_%j.err

###############################################################################
#  Activate Conda
###############################################################################
source ~/miniconda3/bin/activate py310

###############################################################################
# 2️ Local scratch on compute node
###############################################################################
export HF_HOME="$TMPDIR/hf_cache"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export MODEL_DIR="$TMPDIR/DeepSeek"
mkdir -p "$HF_HOME" "$MODEL_DIR"

###############################################################################
# 3️  Download model to $TMPDIR  (doar prima oară pe nod)
##############################################################################
# 4  Download model (TOATE fişierele)
python - <<'PY'
from huggingface_hub import snapshot_download
import pathlib, os, sys
dst = pathlib.Path(os.environ["MODEL_DIR"])
snapshot_download(
    repo_id="unsloth/DeepSeek-R1-Distill-Llama-8B",
    local_dir=str(dst),
    resume_download=True,
)
PY

# 5.  Convert 4-bit dacă nu există deja cele 2 shard-uri
python - <<'PY'
import os, pathlib, sys
MODEL = pathlib.Path(os.environ["MODEL_DIR"])
if not (MODEL / "model-00001-of-00002.safetensors").exists():
    import subprocess, sys
    subprocess.check_call([sys.executable, "pre_convert.py"])
else:
    print("✔  Shard-urile 4-bit există deja.")
PY


###############################################################################
# 6  Launch backend with nohup 
###############################################################################
cd ~/cluster

# Propagăm calea modelului astfel încât app.py s-o poată citi
export MODEL_DIR

# porneşte uvicorn în background
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --log-level debug \
      --access-log > uvicorn.log 2>&1 &

# aşteaptă ca uvicorn să se ridice
sleep 10

# porneşte ngrok exact ca înainte
nohup ./ngrok http 8000 --log=stdout > ngrok.log 2>&1 &

echo "Everything running (PID uvicorn: $(pgrep -f 'uvicorn app'))"
sleep infinity                 # ţine job-ul deschis

