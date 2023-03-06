def update_config():
    from data.config import BOT_TOKEN, imap_server, email_address, password, dirs, admins_id, users_id
    import json
    new_data = {
        'BOT_TOKEN': BOT_TOKEN,
        'IMAP_SERVER': imap_server,
        'EMAIL': email_address,
        'PASSWORD': password,
        'DIRECTORIES': dirs,
        'ADMINS_ID': admins_id,
        'USERS_ID': users_id
    }

    with open('data/config.json', 'w') as file:
        json.dump(new_data, file)
    print("Данные обновлены")