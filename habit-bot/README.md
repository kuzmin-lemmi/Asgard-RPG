# ПривычкаБот — итоговый код курса (урок 9.4)

Бот для привычек: /today, отметки, серии, /stats, добавление через FSM,
погода (/city, /morning), напоминания, логирование ошибок. База — SQLite (`habits.db`, создаётся сама).

## Запуск на VPS (Ubuntu/Debian)

Нужен Python 3.10–3.14 (Ubuntu 22.04 и 24.04 подходят). Проверено на Python 3.12.

```bash
sudo apt update && sudo apt install -y python3 python3-venv
sudo useradd -r -m -d /opt/habit-bot habitbot
# скопируйте содержимое этой папки в /opt/habit-bot (scp, git, rsync)
sudo -u habitbot bash -c 'cd /opt/habit-bot && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt'
sudo -u habitbot cp /opt/habit-bot/.env.example /opt/habit-bot/.env
sudo -u habitbot nano /opt/habit-bot/.env        # вписать BOT_TOKEN
sudo chmod 600 /opt/habit-bot/.env
sudo cp /opt/habit-bot/deploy/habit-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now habit-bot
```

Проверить и смотреть логи:

```bash
sudo systemctl status habit-bot
sudo journalctl -u habit-bot -f
```

Обновить код: скопировать новые файлы и `sudo systemctl restart habit-bot`.

## Демо-версия

В `/start` и `/help` добавлена строка со ссылкой на курс (`COURSE_URL`, `COURSE_NAME`, `COURSE_LINE` в начале `texts.py`). Ещё в демо-версии есть кнопки внизу экрана (`main_keyboard()` в `keyboards.py`, показываются по `/start` и `/menu`) и `bot_profile.py`: при каждом запуске бот сам задаёт меню команд и описание (тексты `BOT_COMMANDS`, `BOT_SHORT_DESCRIPTION`, `BOT_DESCRIPTION` в `texts.py`). Правки описания вносите в `texts.py`: сделанные в BotFather перезапишутся при запуске. Аватарку и картинку к описанию задавайте в BotFather.

`demo.py` и `handlers/demo.py`:

- **лимит привычек:** до 3, задаётся в `MAX_HABITS`; четвёртая не добавится, бот пришлёт `DEMO_LIMIT` со ссылкой на курс;
- **одно сообщение про курс:** `DEMO_NUDGE` в 12:00 по Москве на 3-й день (`NUDGE_TIME`, `NUDGE_AFTER_DAYS`) — только тем, кто добавил хотя бы одну привычку, и только один раз; день первого сообщения хранится в таблице `demo_users`;
- **команда `/inside` и кнопка «🛠 Как устроен»:** какая часть бота — из какого модуля курса.

В коде курса всего этого нет. Чтобы считать переходы из бота отдельно, поменяйте `COURSE_URL` на адрес с меткой и перезапустите бота.

## Важно

- Запускайте бота **в одном экземпляре**: два процесса с одним токеном мешают друг другу.
- Часовой пояс бота задан в `clock.py` (Europe/Moscow) и не зависит от времени сервера.
- Резервная копия базы: `cd /opt/habit-bot && .venv/bin/python backup.py` (можно в cron).
- Тесты: `.venv/bin/pip install pytest && .venv/bin/python -m pytest`.
