from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from news.models import News
from datetime import datetime
from urllib.parse import urljoin

class Command(BaseCommand):
    help = "President.uz bosh sahifasidan so‘nggi yangiliklarni olib keladi"

    def handle(self, *args, **kwargs):
        base_url = "https://president.uz"
        url = base_url + "/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }
        print("Requesting...", url)
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # "So‘nggi yangiliklar" qismi
        main_news_container = soup.find("div", class_="flex-row row")
        print("main_news_container:", bool(main_news_container))
        if not main_news_container:
            self.stdout.write(self.style.ERROR("Yangiliklar konteyneri topilmadi!"))
            return

        news_boxes = main_news_container.find_all("div", class_="events_box")
        print("Topildi:", len(news_boxes), "ta yangilik")

        for box in news_boxes:
            title_tag = box.select_one("a.events_title")
            title = title_tag.text.strip() if title_tag else ""
            link = urljoin(base_url, title_tag['href']) if title_tag else ""

            img_tag = box.select_one("a.events_img img")
            image = urljoin(base_url, img_tag['src']) if img_tag else ""

            date_div = box.select_one("div.date_text")
            published_at = None
            if date_div:
                date_text = date_div.text.strip()
                date_part = date_text.split("|")[0].strip()
                try:
                    published_at = datetime.strptime(date_part, "%d-%m-%Y")
                except Exception as e:
                    print(f"Date parse error: {e}")

            News.objects.update_or_create(
                link=link,
                defaults={
                    "title": title,
                    "description": "",
                    "image": image,
                    "category": "",
                    "published_at": published_at,
                }
            )
            print(f"Saqlanmoqda: {title} | {link}")

        self.stdout.write(self.style.SUCCESS("So‘nggi yangiliklar muvaffaqiyatli saqlandi!"))
