!pip install python-telegram-bot --upgrade
!pip install nest_asyncio

import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import logging

# Configure o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir um dicionário de perguntas e respostas
FAQ = {
    "1": "Eu sou um bot criado para ajudar você!",
    "2": "Eu uso a API do Telegram para receber e responder mensagens.",
    "3": "Eu estou disponível 24/7!",
    "4": "Eu posso responder a perguntas frequentes e interagir com você de várias formas.",
}

# Função que envia o menu de perguntas
async def show_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("1. Qual é o seu nome?", callback_data='1')],
        [InlineKeyboardButton("2. Como você funciona?", callback_data='2')],
        [InlineKeyboardButton("3. Qual é o horário de atendimento?", callback_data='3')],
        [InlineKeyboardButton("4. O que você pode fazer?", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

# Função para lidar com as respostas do menu
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    question_number = query.data
    response = FAQ.get(question_number, "Desculpe, não entendi sua pergunta. Pode reformular?")
    await query.edit_message_text(text=f"Resposta: {response}")

# Função para iniciar o menu quando alguém disser "oi"
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if "oi" in text:
        await show_menu(update, context)

# Função principal para iniciar o bot
def main():
    # Substitua 'YOUR_TOKEN' pelo token do seu bot
    application = Application.builder().token("7295829811:AAHbnfCwyq7JkMtF9QDzO3PJgtyXryJSWns").build()

    # Adicione handlers para mensagens e respostas de botões
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))

    # Inicie o bot
    application.run_polling()

# Execute o bot
if __name__ == '__main__':
    main()
