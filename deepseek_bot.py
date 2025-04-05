import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("7817588593:AAHnCxDdVHmWWiF9ld4du8ZPxr57dJhwIQE")
DEEPSEEK_API_KEY = os.getenv("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")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=DEEPSEEK_API_KEY
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send me a message and I’ll ask DeepSeek-R1!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.6,
            top_p=0.7,
            max_tokens=1024,
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
