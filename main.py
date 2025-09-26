import logging
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import os

# --- CONFIGURAÇÕES ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # define no ambiente ou no Replit
ADMIN_ID = 7742538929  # seu ID de admin do bot

# --- FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase.json")  # coloque seu arquivo json
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Olá {user.first_name}! 👋\nBem-vindo ao bot de investimentos."
    )

async def depositar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("$100", callback_data="deposito_100"),
            InlineKeyboardButton("$300", callback_data="deposito_300"),
        ],
        [
            InlineKeyboardButton("$600", callback_data="deposito_600"),
            InlineKeyboardButton("$1000", callback_data="deposito_1000"),
        ],
        [
            InlineKeyboardButton("$5000", callback_data="deposito_5000"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha o valor para depositar:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("deposito_"):
        valor = query.data.split("_")[1]
        user_id = str(query.from_user.id)

        # salvar no Firestore
        db.collection("investimentos").add({
            "user_id": user_id,
            "valor": int(valor),
            "status": "ativo"
        })

        await query.edit_message_text(text=f"✅ Depósito de ${valor} registrado com sucesso!")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    docs = db.collection("investimentos").where("user_id", "==", user_id).stream()

    investimentos = [f"- ${doc.to_dict()['valor']} ({doc.to_dict()['status']})" for doc in docs]
    if investimentos:
        msg = "📊 Seus investimentos:\n" + "\n".join(investimentos)
    else:
        msg = "❌ Você ainda não tem investimentos."
    await update.message.reply_text(msg)

# --- MAIN ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("depositar", depositar))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
