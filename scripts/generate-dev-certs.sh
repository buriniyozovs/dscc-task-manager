#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${DIR}/dev-certs/live/localhost"
mkdir -p "$OUT"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "${OUT}/privkey.pem" \
  -out "${OUT}/fullchain.pem" \
  -subj "/CN=localhost"
echo "Dev certificates written to ${OUT}"
