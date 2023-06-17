# Телеграм бот для игры в 'Камень, Ножницы, Бумага!'
## Описание
Небольшой PET-проект ТГ бота, в нем реализованы: статистика, профили игроков, таблицы лидеров, правила игры. 
## Технологии
* `Python`
* `aiogram`
* `sqlite3`
## Как запустить
1. Склонируйте репозиторий
2. Создайте и активируйте виртуальное окружение
```commandline 
python -m venv venv
GitBash: source venv/Scripts/activate
Windows: venv\Scripts\activate
Linux: source venv/bin/activate
```
3. Установите зависимости
```commandline 
pip install -r requirements.txt
```
4. Вставьте токен вашего тг бота в файл bot_config.py
```commandline 
TOKEN = '' # Enter your TG bot token here
```
5. Запустите файл main.py
```commandline 
python main.py
```