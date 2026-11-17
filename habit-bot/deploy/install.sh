#!/usr/bin/env bash
# Установка или обновление ПривычкаБота на Ubuntu/Debian.
# Запуск от root из папки с распакованным кодом: bash deploy/install.sh
set -euo pipefail

APP=/opt/habit-bot
SRC="$(cd "$(dirname "$0")/.." && pwd)"

apt-get update -qq
apt-get install -y -qq python3 python3-venv rsync >/dev/null

id habitbot >/dev/null 2>&1 || useradd -r -m -d "$APP" -s /usr/sbin/nologin habitbot
mkdir -p "$APP"

# код — заменяем; .env, habits.db, копии базы и .venv не трогаем
rsync -a --delete \
  --exclude ".env" --exclude "habits.db" --exclude "backup-*.db" --exclude ".venv/" \
  "$SRC"/ "$APP"/
chown -R habitbot:habitbot "$APP"

sudo -u habitbot python3 -m venv "$APP/.venv"
sudo -u habitbot "$APP/.venv/bin/pip" install -q --upgrade pip
sudo -u habitbot "$APP/.venv/bin/pip" install -q -r "$APP/requirements.txt"

if [ ! -f "$APP/.env" ]; then
  sudo -u habitbot cp "$APP/.env.example" "$APP/.env"
fi
chmod 600 "$APP/.env"

cp "$APP/deploy/habit-bot.service" /etc/systemd/system/habit-bot.service
systemctl daemon-reload
systemctl enable habit-bot >/dev/null

if grep -q "вставьте_сюда" "$APP/.env"; then
  echo
  echo "Готово, но токена ещё нет. Впишите его:  nano $APP/.env"
  echo "Затем запустите:                         systemctl restart habit-bot"
else
  systemctl restart habit-bot
  sleep 3
  systemctl --no-pager --lines=5 status habit-bot || true
fi
