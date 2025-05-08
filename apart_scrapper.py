import requests
from bs4 import BeautifulSoup
import re

def get_avito_flats(city="Casablanca", max_price=None, min_price=None, min_surface=None):
    base_url = "https://www.avito.ma/fr"
    city_path = city.lower().replace(" ", "_")
    url = f"{base_url}/{city_path}/appartements-%C3%A0_vendre"
    listings = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch Avito listings")

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("a.sc-1jge648-0")

    for card in cards:
        try:
            title_el = card.find("p", attrs={"title": True})
            title = title_el.text.strip() if title_el else "N/A"

            price_el = card.select_one("p.sc-1x0vz2r-0.dJAfqm")
            price_text = price_el.text.strip() if price_el else ""
            price = int(re.sub(r"[^0-9]", "", price_text)) if price_text else 0

            link = card.get("href")
            link = base_url + link if link else ""

            details_text = card.get_text(" ", strip=True).lower()
            surface_match = re.search(r"(\d{2,4})\s?m\u00b2", details_text)
            surface = int(surface_match.group(1)) if surface_match else None

            if min_price and price < min_price:
                continue
            if max_price and price > max_price:
                continue
            if min_surface and (surface is None or surface < min_surface):
                continue

            listings.append({
                "title": title,
                "price": price,
                "surface": surface,
                "price_per_m2": round(price / surface, 2) if surface else None,
                "link": link
            })
        except Exception:
            continue

    listings.sort(key=lambda x: x["price_per_m2"] or float("inf"))
    return listings
