from imaplib import IMAP4_SSL
import email
from data.config import imap_server, email_address, password, dirs

imap = IMAP4_SSL(imap_server)
imap.login(email_address, password)

imap.select(dirs[0])
_, msgnums = imap.search(None, "ALL")

for msgnum in msgnums[0].split():
    _, data = imap.fetch(msgnum, "(RFC822)")

    message = email.message_from_bytes(data[0][1])

    print(f"Message number: {msgnum}")
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"BCC: {message.get('BCC')}")
    print(f"From: {message.get('From')}")





