BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Respect ethical scraping guidelines
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2  # Rate limiting (2 seconds delay)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

ITEM_PIPELINES = {
   'scraper.pipelines.PostgresPipeline': 300,
}