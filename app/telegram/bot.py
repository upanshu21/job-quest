import os
import telegram
from dotenv import load_dotenv

class NotificationTelegram:
    """
    Class to send notifications to a Telegram channel.
    """
    def __init__(self):
        load_dotenv()
        self.bot = telegram.Bot(token=os.getenv('BOT_TOKEN'))
        self.chat_id = os.getenv('CHAT_ID')

    async def send_message(self, text):
        await self.bot.send_message(text=text, chat_id=self.chat_id)

    async def send_job_notification(self, job_data):
        """Format and send job notification"""
        message = (
            f"🆕 New Job Alert!\n\n"
            f"📋 Title: {job_data['title']}\n"
            f"🔍 ID: {job_data['id']}\n"
            f"⏰ {job_data['posted_on']}\n"
            f"🔗 {job_data['url']}"
        )
        await self.send_message(message)
