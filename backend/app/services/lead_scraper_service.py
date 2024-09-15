import asyncio
import random
from playwright.async_api import async_playwright, Playwright, Browser, Page
from bs4 import BeautifulSoup
from app.schemas.lead import LeadCreate
from app.core.config import settings
from typing import List, Dict
import logging

class LeadScraperService:
    def __init__(self):
        self.browser: Browser | None = None
        self.context: Browser | None = None
        self.proxies: List[str] = []
        self.current_proxy: str | None = None
        self.linkedin_email: str = []
        self.linkedin_password: str = []

    async def initialize(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def rotate_proxy(self):
        if self.context:
            await self.context.close()
        self.current_proxy = random.choice(self.proxies)
        self.context = await self.browser.new_context(proxy={"server": self.current_proxy})

       async def login_linkedin(self, page: Page, email: str, password: str):
        await page.goto("https://www.linkedin.com/login")
        await page.fill('input[name="session_key"]', email)
        await page.fill('input[name="session_password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_navigation()

    async def set_linkedin_cookies(self, cookies: List[Dict]):
        if self.context:
            await self.context.add_cookies(cookies)

    async def scrape_linkedin(self, search_query: str, max_results: int = 10, email: str = None, password: str = None, cookies: List[Dict] = None) -> List[LeadCreate]:
        if not self.browser:
            await self.initialize()

        await self.rotate_proxy()
        page = await self.context.new_page()
        
        if cookies:
            await self.set_linkedin_cookies(cookies)
        elif email and password:
            await self.login_linkedin(page, email, password)
        else:
            raise ValueError("Either cookies or email/password must be provided")

        leads: List[LeadCreate] = []
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}&origin=GLOBAL_SEARCH_HEADER"
        await page.goto(search_url)

        while len(leads) < max_results:
            await self.scroll_and_extract(page, leads, max_results)
            if len(leads) < max_results:
                if not await self.next_page(page):
                    break

        detailed_leads = await self.enrich_leads(leads[:max_results])
        await page.close()
        return detailed_leads


        async def scrape_twitter(self, search_query: str, max_results: int = 10) -> list[LeadCreate]:
        if not self.context:
            await self.initialize()

        page = await self.context.new_page()
        await page.goto(f"https://twitter.com/search?q={search_query}&f=user")
        await page.wait_for_selector('.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2')

        leads = []
        while len(leads) < max_results:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)  # Wait for new content to load

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            user_cells = soup.select('.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2')

            for cell in user_cells:
                if len(leads) >= max_results:
                    break

                name_elem = cell.select_one('.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')
                handle_elem = cell.select_one('.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0:not(.r-1awozwy)')
                
                if name_elem and handle_elem:
                    name = name_elem.text.strip()
                    twitter_handle = handle_elem.text.strip()
                    
                    lead = LeadCreate(
                        name=name,
                        twitter_handle=twitter_handle
                    )
                    leads.append(lead)

        await page.close()
        return leads


   async def scrape_linkedin(self, search_query: str, max_results: int = 10, email: str = None, password: str = None, cookies: List[Dict] = None) -> List[LeadCreate]:
        if not self.browser:
            await self.initialize()

        await self.rotate_proxy()
        page = await self.context.new_page()
        
        if cookies:
            await self.set_linkedin_cookies(cookies)
        elif email and password:
            await self.login_linkedin(page, email, password)
        else:
            raise ValueError("Either cookies or email/password must be provided")

        leads: List[LeadCreate] = []
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}&origin=GLOBAL_SEARCH_HEADER"
        await page.goto(search_url)

        while len(leads) < max_results:
            await self.scroll_and_extract(page, leads, max_results)
            if len(leads) < max_results:
                if not await self.next_page(page):
                    break

        detailed_leads = await self.enrich_leads(leads[:max_results])
        await page.close()
        return detailed_leads


    async def scroll_and_extract(self, page: Page, leads: List[LeadCreate], max_results: int):
        last_height = await page.evaluate("document.body.scrollHeight")
        while len(leads) < max_results:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            results = soup.select('.reusable-search__result-container')

            for result in results:
                if len(leads) >= max_results:
                    break
                lead = await self.extract_lead_info(result)
                if lead:
                    leads.append(lead)

    async def next_page(self, page: Page) -> bool:
        next_button = await page.query_selector('button[aria-label="Next"]')
        if next_button:
            await next_button.click()
            await page.wait_for_load_state('networkidle')
            return True
        return False

    async def extract_lead_info(self, result) -> LeadCreate | None:
        try:
            name_elem = result.select_one('.app-aware-link > span > span')
            title_elem = result.select_one('.entity-result__primary-subtitle')
            company_elem = result.select_one('.entity-result__secondary-subtitle')
            linkedin_url_elem = result.select_one('.app-aware-link')
            
            if name_elem and linkedin_url_elem:
                return LeadCreate(
                    name=name_elem.text.strip(),
                    linkedin_url=linkedin_url_elem['href'],
                    position=title_elem.text.strip() if title_elem else None,
                    company=company_elem.text.strip() if company_elem else None
                )
        except Exception as e:
            logging.error(f"Error extracting lead info: {e}")
        return None

    async def enrich_leads(self, leads: List[LeadCreate]) -> List[LeadCreate]:
        enriched_leads = []
        for lead in leads:
            try:
                await asyncio.sleep(random.uniform(1, 3))  # Random delay to avoid detection
                page = await self.context.new_page()
                await page.goto(lead.linkedin_url)
                await page.wait_for_load_state('networkidle')

                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')

                # Extract more detailed information
                about_section = soup.select_one('section.summary')
                if about_section:
                    lead.about = about_section.text.strip()

                experience_section = soup.select_one('section.experience')
                if experience_section:
                    experiences = experience_section.select('li.experience-item')
                    lead.experience = [exp.text.strip() for exp in experiences[:3]]  # Get last 3 experiences

                education_section = soup.select_one('section.education')
                if education_section:
                    educations = education_section.select('li.education-item')
                    lead.education = [edu.text.strip() for edu in educations]

                # Try to find email (this is a simplified approach and might not always work)
                email_elem = soup.select_one('section.contact-info a[href^="mailto:"]')
                if email_elem:
                    lead.email = email_elem['href'].replace('mailto:', '')

                enriched_leads.append(lead)
                await page.close()

            except Exception as e:
                logging.error(f"Error enriching lead {lead.name}: {e}")
                enriched_leads.append(lead)

        return enriched_leads

lead_scraper = LeadScraperService()