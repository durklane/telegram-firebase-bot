import firebase_admin
from firebase_admin import credentials, firestore
from telegram.ext import Updater, CommandHandler

# Configurações
ADMIN_ID = 7742538929  # teu ID de admin

# Conectar ao Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # arquivo que tu vais baixar do Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Comando /start
def start(update, context):
    update.message.reply_text("✅ Bot conectado com Firebase!")

def main():
    # Coloca teu token do Telegram aqui
    updater = Updater("COLOCA_TEU_TOKEN_AQUI", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
