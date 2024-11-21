# sferum_bot
Get a token from Selenium and send a message to selected chats
# Docker
Для автоматизации был создан образ
```
 lisrui/sferum_bot:1.0
```
Для корректной работы необходимо создать директорию для хранения данных.
```bash
 mkdir -p /bot/data/changes
```
Внутри /bot/data необходимо создать файл .env с данными для аутентификации со следующей структурой:
```
number=""
pass=""
hash_vk=""
token=""
chat_id=""
```
Для пулла образа:
```bash
docker run -v /bot/data:/app/data --name sferum_bot lisrui/sferum_bot:1.0
```
Для запуска используйте:
```bash
docker start sferum_bot
```
