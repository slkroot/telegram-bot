import os
import time
import random
import asyncio
import schedule
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

# Configurações do bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1002303381759"
IMAGES_FOLDER = "images"
IMAGES_FILE = "image_list.txt"
DESCRIPTIONS_FILE = "descriptions_list.txt"

bot = Bot(token=BOT_TOKEN)

def load_list_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado!")
        return []
    
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Carregar imagens e descrições aleatórias
image_list = load_list_from_file(IMAGES_FILE)
description_list = load_list_from_file(DESCRIPTIONS_FILE)

def shuffle_and_cycle(lst):
    random.shuffle(lst)
    while True:
        for item in lst:
            yield item

image_cycle = shuffle_and_cycle(image_list)
description_cycle = shuffle_and_cycle(description_list)

async def send_image():
    if not image_list or not description_list:
        print("Nenhuma imagem ou descrição disponível para envio.")
        return

    image_name = next(image_cycle)  # Escolhe imagem sem repetir até rodar todas
    caption = next(description_cycle)  # Escolhe descrição sem repetir até rodar todas
    image_path = os.path.join(IMAGES_FOLDER, image_name)

    if not os.path.exists(image_path):
        print(f"Imagem {image_name} não encontrada no caminho {image_path}!")
        return

    try:
        with open(image_path, "rb") as img:
            button = InlineKeyboardButton("CLIQUE AQUI ", url="https://larissaa.site/contato")
            markup = InlineKeyboardMarkup([[button]])
            
            await bot.send_photo(chat_id=CHAT_ID, photo=img, caption=caption, reply_markup=markup, parse_mode="MarkdownV2")
            print(f"Imagem {image_name} enviada com sucesso!")
    except TelegramError as e:
        print(f"Erro ao enviar imagem: {e}")

async def scheduler():
    while True:
        await send_image()
        await asyncio.sleep(5400)  # Tempo entre envios (20 segundos para testes, mude para 5400 para 1h30min)

print("Bot iniciado. Enviando uma imagem...")

asyncio.run(send_image())  # Envia apenas uma imagem por execução

