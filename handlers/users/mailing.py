from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from imaplib import IMAP4_SSL
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
import quopri

from loader import dp
from States import CommonStates
from data.config import imap_server, email_address, password, dirs, users_id, admins_id


@dp.message_handler(Command('start_mailing'))
async def start_mailing(message: types.Message):
    if message.from_user.id in admins_id:
        await CommonStates.mailing.set()
    else:
        await message.answer("Вы не являетесь администратором")


@dp.message_handler(state=CommonStates.mailing)
async def getting_mails(message: types.Message, state: FSMContext):
    await message.answer("Рассылка запущена", reply_markup=None)
    imap = connection()
    status, messages = imap.select(dirs[0])
    res, unseen_msg = imap.uid("search", "UNSEEN", "ALL")
    unseen_msg = unseen_msg[0].decode("utf-8").split(" ")

    if unseen_msg[0]:
        for letter in unseen_msg:
            res, msg = imap.uid("fetch", letter, "(RFC822)")
            if res == "OK":
                msg = email.message_from_bytes(msg[0][1])
                msg_from = from_subj_decode(msg['From'])
                msg_subj = from_subj_decode(msg['Subject'])
                if msg['Message-ID']:
                    msg_id = msg['Message-ID'].lstrip("<").rstrip(">")
                else:
                    msg_id = msg['Received']
                if msg['Return-path']:
                    msg_email = msg['Return-path'].lstrip("<").rstrip(">")
                else:
                    msg_email = msg_from

                if not msg_email:
                    encoding = decode_header(msg["From"])[0][1]
                    msg_email = (
                        decode_header(msg['From'])[1][0]
                        .decode(encoding)
                        .replace("<", "")
                        .replace(">", "")
                        .replace(" ", "")
                    )
                letter_text = get_letter_text(msg)
                attachments = get_attachments(msg)

                post_text = post_construct(msg_subj, msg_from, msg_email, letter_text, attachments)

                if len(post_text) > 4000:
                    post_text = post_text[:4000]

                for user_id in users_id:
                    dp.bot.send_message(text=post_text, chat_id=user_id)

        imap.logout()
    else:
        imap.logout()


def connection():
    imap = IMAP4_SSL(imap_server)
    sts, res = imap.login(email_address, password)
    if sts == 'OK':
        return imap
    else:
        return False

def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


def encode_att_names(str_pl):
    enode_name = re.findall("\=\?.*\?\=", str_pl)
    if len(enode_name) == 1:
        encoding = decode_header(enode_name[0])[0][1]
        decode_name = decode_header(enode_name[0])[0][0]
        decode_name = decode_name.decode(encoding)
        str_pl = str_pl.replace(enode_name[0], decode_name)
    if len(enode_name) > 1:
        nm = ""
        for part in enode_name:
            encoding = decode_header(part)[0][1]
            decode_name = decode_header(part)[0][0]
            decode_name = decode_name.decode(encoding)
            nm += decode_name
        str_pl = str_pl.replace(enode_name[0], nm)
        for c, i in enumerate(enode_name):
            if c > 0:
                str_pl = str_pl.replace(enode_name[c], "").replace('"', "").rstrip()
    return str_pl


def get_attachments(msg):
    attachments = list()
    for part in msg.walk():
        if (
                part["Content-Type"]
                and "name" in part["Content-Type"]
                and part.get_content_disposition() == 'attachment'
        ):
            str_pl = part["Content-Type"]
            str_pl = encode_att_names(str_pl)
            attachments.append(str_pl)
    return attachments


def get_letter_text_from_html(body):
    body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("div")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + '\n'
        return text.replace("\xa0", " ")
    except (Exception) as exp:
        print("text from html err ", exp)
        return False


def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = get_letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", "")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = get_letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part.rstrip().lstrip()
            count += 1
            return (
                letter_text.replace("<", "").replace(">", "").replace("\xa0", "")
            )


def get_letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:
        return part.get_payload()


def post_construct(msg_subj, msg_from, msg_email, letter_text, attachments):
    att_txt = "\n".join(attachments)
    post_parts = [
        "\U0001F4E8 <b>",
        str(msg_subj),
        "</b>\n\n",
        "<pre>",
        str(msg_from),
        "\n",
        msg_email,
        "</pre>\n\n",
        letter_text,
        "\n\n",
        att_txt
    ]
    return "".join(post_parts)
