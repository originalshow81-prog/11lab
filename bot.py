import os
import sys
import asyncio
import tempfile
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

user_voices = {}
user_voice_names = {}


def get_voices():
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    r = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=10)
    if r.status_code == 200:
        return r.json().get("voices", [])
    return []


def tts(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code == 200:
        return r.content
    return None


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salut! Trimite-mi orice text si il trimit inapoi ca mesaj vocal.\n\n"
        "Comenzi:\n/voice - alege vocea\n/currentvoice - vocea activa acum"
    )


async def cmd_current_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    vid = user_voices.get(uid, DEFAULT_VOICE_ID)
    name = user_voice_names.get(uid, "Rachel (implicit)")
    await update.message.reply_text(f"Voce activa: {name}\nID: {vid}")


async def cmd_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Incarc vocile din ElevenLabs...")
    voices = get_voices()
    if not voices:
        await msg.edit_text("Eroare la incarcarea vocilor. Verifica API key-ul.")
        return
    buttons = []
    row = []
    for v in voices[:24]:
        row.append(InlineKeyboardButton(v["name"], callback_data=f"sv|{v['voice_id']}|{v['name']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    await msg.edit_text("Alege o voce:", reply_markup=InlineKeyboardMarkup(buttons))


async def callback_set_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("|", 2)
    if len(parts) != 3:
        return
    _, voice_id, voice_name = parts
    user_voices[query.from_user.id] = voice_id
    user_voice_names[query.from_user.id] = voice_name
    await query.edit_message_text(f"Voce setata: {voice_name}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id
    voice_id = user_voices.get(uid, DEFAULT_VOICE_ID)
    status = await update.message.reply_text("Generez vocea...")
    audio = tts(text, voice_id)
    if audio is None:
        await status.edit_text("Eroare ElevenLabs. Verifica cheia API sau limita lunara.")
        return
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio)
        tmp = f.name
    try:
        with open(tmp, "rb") as f:
            await update.message.reply_voice(voice=f)
        await status.delete()
    finally:
        os.unlink(tmp)


async def run():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN lipseste din .env")
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY lipseste din .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("voice", cmd_voice))
    app.add_handler(CommandHandler("currentvoice", cmd_current_voice))
    app.add_handler(CallbackQueryHandler(callback_set_voice, pattern=r"^sv\|"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot pornit. Apasa Ctrl+C pentru oprire.")
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Event().wait()
        await app.updater.stop()
        await app.stop()


if __name__ == "__main__":
    asyncio.run(run())
