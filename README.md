# e_mail_bot

Бот пересылает непрочитанные письма из указанных каталогов электронной почты пользователям из списка users_id. 
Пользователи из списка admins_id могут добавлять новых пользователей и администраторов, запускать и отключать рассылку,
изменять e-mail адрес и каталоги, из которых собираются письма.

Установка:

    git clone https://github.com/elstds/e_mail_bot
    cd e_mail_bot
    python ini.py
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python main.py

