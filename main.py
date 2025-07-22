import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME")

# Configuración de Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credenciales.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# Configurar logging
logging.basicConfig(level=logging.INFO)

async def fichar(update: Update, context: ContextTypes.DEFAULT_TYPE, accion: str):
    usuario = update.effective_user.full_name
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, usuario, accion])
    await update.message.reply_text(f"✅ Has fichado: {accion.upper()} a las {timestamp}")

async def entrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await fichar(update, context, "entrar")

async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await fichar(update, context, "salir")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Usa /entrar o /salir para fichar.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("entrar", entrar))
    app.add_handler(CommandHandler("salir", salir))

    print("✅ Bot funcionando en Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
