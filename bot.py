import logging
import schedule
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from entertainment import EntertainmentScraper
from home_page import WebScraper as HomePageScraper
from sports import WebScraper as SportsScraper
from education import WebScraper as EducationScraper

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your Telegram bot token
TOKEN = 'YOUR TOKEN KEY'
# Define your ChatID
CHAT_ID = 'YOUR CHAT ID'

# Create instances of the scrapers
entertainment_scraper = EntertainmentScraper("https://timesofindia.indiatimes.com/")
home_page_scraper = HomePageScraper("https://timesofindia.indiatimes.com/etimes")
sports_scraper = SportsScraper("https://timesofindia.indiatimes.com/sports")
education_scraper = EducationScraper("https://timesofindia.indiatimes.com/education")

# Define command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Headlines Bot! Type /entertainment for Entertainment headlines, /home for Home page headlines, or /sports for Sports headlines.')

def send_entertainment_news(update: Update, context: CallbackContext) -> None:
    try:
        html_content = entertainment_scraper.fetch_webpage()
        print(html_content)
        headlines = entertainment_scraper.extract_headlines(html_content)
        context.bot.send_message(chat_id=context.job.context, text="\n".join(headlines))
    except Exception as e:
        logger.error(e)

def send_home_page_news(context: CallbackContext) -> None:
    try:
        html_content = home_page_scraper.fetch_webpage()
        headlines = home_page_scraper.extract_headlines(html_content)
        context.bot.send_message(chat_id=context.job.context, text="\n".join(headlines))
    except Exception as e:
        logger.error(e)

def send_sports_news(context: CallbackContext) -> None:
    try:
        html_content = sports_scraper.fetch_webpage()
        headlines = sports_scraper.extract_headlines(html_content)
        context.bot.send_message(chat_id=context.job.context, text="\n".join(headlines))
    except Exception as e:
        logger.error(e)

def send_education_news(context: CallbackContext) -> None:
    try:
        html_content = education_scraper.fetch_webpage()
        headlines = education_scraper.extract_headlines(html_content)
        context.bot.send_message(chat_id=context.job.context, text="\n".join(headlines))
    except Exception as e:
        logger.error(e)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("entertainment", send_entertainment_news))
    application.add_handler(CommandHandler("home", send_home_page_news))
    application.add_handler(CommandHandler("sports", send_sports_news))
    application.add_handler(CommandHandler("education", send_education_news))

    # Schedule the news updates
    application.job_queue.run_daily(send_entertainment_news, time=datetime.time(hour=10, minute=22, second=00), days=(0, 1, 2, 3, 4, 5, 6))
    application.job_queue.run_daily(send_home_page_news, time=datetime.time(hour=9, minute=23,second=00),days=(0, 1, 2, 3, 4, 5, 6))
    application.job_queue.run_daily(send_sports_news, time=datetime.time(hour=10,minute=24,second=00),days=(0, 1, 2, 3, 4, 5, 6))
    application.job_queue.run_daily(send_education_news, time=datetime.time(hour=10,minute=24,second=00),days=(0, 1, 2, 3, 4, 5, 6))

    # Start the Bot
    application.run_polling()
    application.idle()

if __name__ == '__main__':
    main()
