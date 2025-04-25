from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pandas as pd
import os

# קישור לקובץ Google Sheets שפורסם כ-CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQphC-7fqUG6ZJmdkDTn8tkvGu88LrIlzaij3jL48kbAOud8SEe3xnyCgVbf0OcSJuPmpdM_0qKN525/pub?output=csv"

# טען את קובץ המושגים מהשיטס
def load_glossary():
    df = pd.read_csv(CSV_URL)
    return dict(zip(df['מונח'].str.lower(), df['הסבר']))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    glossary = load_glossary()
    
    if context.args:
        term = context.args[0].lower()
        definition = glossary.get(term, "❌ לא מצאתי הגדרה למושג הזה. נסה מונח אחר.")
    else:
        definition = "ברוך הבא לבוט המילון של הקפיטליסטים 📘\nשלח מונח או השתמש בקישורים מהערוץ."

    await update.message.reply_text(definition)

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()