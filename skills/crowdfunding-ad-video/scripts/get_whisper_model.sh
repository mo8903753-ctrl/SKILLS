#!/bin/bash
# Download the faster-whisper "base" model via hf-mirror.com (huggingface.co downloads stall on this network).
# Usage: get_whisper_model.sh [small|base]   → ~/.cache/adkit/fw-<size>
set -e
SIZE=${1:-base}
DST=~/.cache/adkit/fw-$SIZE
mkdir -p "$DST"
for f in config.json tokenizer.json vocabulary.txt model.bin; do
  if [ ! -s "$DST/$f" ]; then
    curl -sL --retry 3 --max-time 900 -o "$DST/$f" "https://hf-mirror.com/Systran/faster-whisper-$SIZE/resolve/main/$f"
  fi
  echo "$f $(du -h "$DST/$f" | cut -f1)"
done
python3 -c "import faster_whisper" 2>/dev/null || echo "faster_whisper missing: pip3 install faster-whisper"
echo "model dir: $DST"
