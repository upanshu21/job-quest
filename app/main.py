from app.scraper import JobScraperApp
import asyncio

async def main():
    app = JobScraperApp()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())