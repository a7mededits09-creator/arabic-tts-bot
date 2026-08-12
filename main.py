import asyncio
import edge_tts
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8792747895:AAH3LQ3YDxC5eblm2B-pf9DsgNGXGjBulXE"
VOICE = "ar-EG-ShakirNeural"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي النص وسأقوم بتحويله لصوت حماسي.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    output_file = f"voice_{user_id}.mp3"
    
    await update.message.reply_chat_action("record_voice")
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)
        
        with open(output_file, "rb") as audio:
            await update.message.reply_voice(voice=audio)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text("حدث خطأ أثناء تحويل النص.")
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("البوت يعمل على السيرفر...")
    app.run_polling()
