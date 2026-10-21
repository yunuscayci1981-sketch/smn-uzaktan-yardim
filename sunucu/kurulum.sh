#!/usr/bin/env bash
# SMN Bilişim Uzaktan Yardım - sunucu kurulumu (Ubuntu 22.04 / 24.04, Debian 12)
# Kullanım:  sudo bash kurulum.sh uzak.smnbilisim.com
set -euo pipefail

ALAN_ADI="${1:-uzak.smnbilisim.com}"
HEDEF=/opt/smn-uzaktan-yardim
KAYNAK="$(cd "$(dirname "$0")" && pwd)"

if [ "$(id -u)" -ne 0 ]; then
  echo "Lütfen sudo ile çalıştırın: sudo bash kurulum.sh $ALAN_ADI"; exit 1
fi

echo ">> Docker kuruluyor..."
if ! command -v docker >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y ca-certificates curl
  curl -fsSL https://get.docker.com | sh
fi

echo ">> Dosyalar $HEDEF içine kopyalanıyor..."
mkdir -p "$HEDEF/data"
cp "$KAYNAK/docker-compose.yml" "$HEDEF/"
if [ ! -f "$HEDEF/data/id_ed25519" ]; then
  cp "$KAYNAK/data/id_ed25519" "$KAYNAK/data/id_ed25519.pub" "$HEDEF/data/"
fi
chmod 600 "$HEDEF/data/id_ed25519"
echo "SMN_ALAN_ADI=$ALAN_ADI" > "$HEDEF/.env"

echo ">> Güvenlik duvarı portları açılıyor..."
if command -v ufw >/dev/null 2>&1; then
  ufw allow 22/tcp >/dev/null
  ufw allow 21114:21119/tcp >/dev/null
  ufw allow 21116/udp >/dev/null
  ufw --force enable >/dev/null
fi

echo ">> Sunucu başlatılıyor..."
cd "$HEDEF"
docker compose pull
docker compose up -d

sleep 3
echo
echo "=============================================="
echo " SMN Uzaktan Yardım sunucusu çalışıyor"
echo " Alan adı : $ALAN_ADI"
echo " Anahtar  : $(cat "$HEDEF/data/id_ed25519.pub")"
echo "=============================================="
docker compose ps
