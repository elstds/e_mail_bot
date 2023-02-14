import json

with open('data/config.json', 'r') as file:
    config = json.load(file)

BOT_TOKEN = config['BOT_TOKEN']
imap_server = config['IMAP_SERVER']
email_address = config['EMAIL']
password = config['PASSWORD']
dirs = config['DIRECTORIES']

admins_id = config['ADMINS_ID']

users_id = config['USERS_ID']
