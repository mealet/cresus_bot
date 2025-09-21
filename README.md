# 📑 Cresus Craft Discord Bot
Cresus Craft Bot - простой дискорд бот для сервера проекта "Cresus Craft". <br/>
Вся документация и сообщения написаны на русском языке для локальных разработчиков.

## ⚙️ Техническая Информация
- **Пакетный Менеджер:** **`uv`**
- **Линтер/Чекер:** **`ruff`**
- **Библиотека для Дискорд:** **`nextcord`**
- **Логирование:** **`loguru`**
- **База Данных:** **`aiosqlite`** (асинхронная SQLite, как поставить другую читайте в `src/database/client.py`)

## ✨ Установка
### Через Docker (рекомендутся)
1. Установите [Docker](https://www.docker.com/) и плагин [Docker Compose](https://docs.docker.com/compose/install/)
2. Клонируйте проект локально и зайдите в него:
```command
git clone https://github.com/mealet/cresus_bot
cd cresus_bot
```
3. Настройте под себя конфиги (смотрите `src/config.py`)
4. Поставьте токен от бота в переменную окружения, или создайте файл `.env` в корне:
```env
CRESUS_BOT_TOKEN=ВАШ_ТОКЕН
```
5. Соберите образ:
```command
docker compose build
```
6. Запустите бота:
```command
# Интерактивный режим
docker compose up

# В фоне
docker compose up -d
```

### Через uv
1. Установите пакетный менеджер (uv)[https://docs.astral.sh/uv/]
2. Синронизируйте зависимости:
```command
uv sync
```
3. Запустите бота:
```command
# Только в интерактивном режиме (в фоне самому настраивать)
uv run main.py
```

## 👮 Лицензия
Проект лицензирован под лицензией Apache 2.0 <br/>
Вся информация в файле [LICENSE](LICENSE)
