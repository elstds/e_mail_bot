from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from imaplib import IMAP4_SSL
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re

from loader import dp
from States import BotStates
from data.config import imap_server, email_address, password, dirs


@dp.message_handler(Command('start_mailing'))
async def start_mailing(message: types.Message):
    await BotStates.mailing.set()


@dp.message_handler(state=BotStates.mailing)
async def getting_mails(message: types.Message, state: FSMContext):
    await message.answer("Рассылка запущена")
    imap = IMAP4_SSL(imap_server)
    imap.login(email_address, password)
    imap.select(dirs[0])

    _, msg_nums = imap.search(None, "ALL")

    for num in msg_nums[0].split():
        _, data = imap.fetch(num, "(RFC822)")
        mail = email.message_from_bytes(data[0][1])
        await message.answer(
            f"Message number: {num}\nFrom: {decode_header(mail['From'])[0][0].decode()}\nTo: {decode_header(mail['To'])[0][0]}\nBCC: {mail.get('BCC')}\nSubject: {decode_header(mail['Subject'])[0][0].decode()}")
