import os
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

class PostgresPipeline:
    def __init__(self):
        models.Base.metadata.create_all(bind=engine)
        self.db = None

    def open_spider(self):
        self.db: Session = SessionLocal()

    def close_spider(self):
        if self.db:
            self.db.close()

    def process_item(self, item):
        existing_product = self.db.query(models.ProductPrice).filter_by(url=item['url']).first()

        if existing_product:
            if existing_product.price != item['price']:
                old_price = existing_product.price
                existing_product.price = item['price']
                existing_product.availability = item['availability']
                self.db.commit()
                self.send_alert(item['title'], old_price, item['price'], item['url'])
        else:
            new_product = models.ProductPrice(
                title=item['title'],
                price=item['price'],
                availability=item['availability'],
                url=item['url']
            )
            self.db.add(new_product)
            self.db.commit()

        return item

    def send_alert(self, title, old_price, new_price, url):
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook_url or "discord" not in webhook_url:
            print(f"ALERT: {title} price changed from ${old_price} to ${new_price}")
            return

        message = {
            "content": f"🚨 **Price Alert!** 🚨\n**Product:** {title}\n**Old Price:** ${old_price}\n**New Price:** ${new_price}\n**Link:** {url}"
        }
        try:
            requests.post(webhook_url, json=message, timeout=5)
        except Exception as e:
            print(f"Failed to send webhook: {e}")