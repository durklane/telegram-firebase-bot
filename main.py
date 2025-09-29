import firebase_admin
from firebase_admin import credentials, firestore
from telegram.ext import Updater, CommandHandler

# ID do administrador
ADMIN_ID = 7742538929  

# Conectar ao Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # <<< Arquivo do Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Comando /start
def start(update, context):
    update.message.reply_text("✅ Bot conectado com Firebase!")

def main():
    updater = Updater("AAEtOkC_Ei4Bhp3eMBlxx_gRyfDnZz1BI9Q"), use_context=True)  # <<< Teu token aqui
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
