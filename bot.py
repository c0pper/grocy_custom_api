import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from retrieving import chain
from dotenv import load_dotenv
import logging


from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

load_dotenv()


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = chain.invoke(update.message.text)
    await update.message.reply_text(response)


app = ApplicationBuilder().token(os.getenv("TELE_TOKEN")).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()