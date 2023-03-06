import json

bot_token = input("Введите токен бота: ")
print("=" * 80)
first_admin_id = int(input("Введите id первого администратора: "))
print("=" * 80)
imap_server = input("Введите адресс imap-сервера (imap.google.com): ")
print("=" * 80)
email_address = input("Введите e-mail адресс: ")
print("=" * 80)
password = input("Введите пароль: ")
print("=" * 80)
dirs = input("Введите названия каталогов, из которых бот будет собирать сообщения,  через пробел: ").split()
print("=" * 80)
print("Конфигурация бота закончена!")
config = {
    'BOT_TOKEN': bot_token,
    'ADMINS_ID': [first_admin_id],
    'IMAP_SERVER': imap_server,
    'EMAIL': email_address,
    'PASSWORD': password,
    'DIRECTORIES': dirs,
    'USERS_ID': []

}

with open('data/config.json', 'w') as file:
    json.dump(config, file)


