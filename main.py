import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuración
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME", "fichajes")
CREDS_FILE = "credenciales.json"

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# Comando /fichar
async def fichar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre = f"{user.first_name or ''} {user.last_name or ''}".strip()

    sheet.append_row([timestamp, nombre])
    await update.message.reply_text(f"✅ {nombre}, fichaje registrado a las {timestamp}")

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("fichar", fichar))
    app.run_polling()

if __name__ == "__main__":
    main()
