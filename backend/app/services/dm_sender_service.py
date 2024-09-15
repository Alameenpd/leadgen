import asyncio
from playwright.async_api import async_playwright
from app.models.campaign import Campaign
from app.models.lead import Lead
from app.services.analytics_service import update_analytics
from app.database import SessionLocal
from typing import List
import logging

class DMService:
    def __init__(self):
        self.browser = None
        self.context = None

    async def initialize(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def login_linkedin(self, page, email: str, password: str):
        await page.goto("https://www.linkedin.com/login")
        await page.fill('input[name="session_key"]', email)
        await page.fill('input[name="session_password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_navigation()

    async def send_dm(self, lead: Lead, message: str):
        page = await self.context.new_page()
        try:
            await page.goto(f"https://www.linkedin.com/messaging/compose/?connId={lead.linkedin_id}&messageCompose=")
            await page.fill('div[aria-label="Write a message…"]', message)
            await page.click('button[type="submit"]')
            await page.wait_for_selector('div[aria-label="Conversation"]')
            return True
        except Exception as e:
            logging.error(f"Error sending DM to {lead.name}: {str(e)}")
            return False
        finally:
            await page.close()
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def send_dm(self, lead: Lead, message: str):
      
    async def process_campaign(self, campaign: Campaign, email: str, password: str):
        if not self.browser:
            await self.initialize()

        page = await self.context.new_page()
        await self.login_linkedin(page, email, password)
        await page.close()

        db = SessionLocal()
        try:
            user = campaign.user
            dm_limit = check_user_limit(user, "dms")
            sent_dms = 0

            for lead in campaign.leads:
                if sent_dms >= dm_limit:
                    logging.warning(f"DM limit reached for user {user.id}")
                    break

                message = campaign.message_template.format(name=lead.name, company=lead.company)
                try:
                    success = await self.send_dm(lead, message)
                    if success:
                        update_analytics(db, campaign.user_id, campaign.id, messages_sent=1)
                        sent_dms += 1
                except Exception as e:
                    logging.error(f"Error sending DM to {lead.name}: {str(e)}")
                
                await asyncio.sleep(random.uniform(30, 60))  # Random delay between messages
        finally:
            db.close()


dm_service = DMService()