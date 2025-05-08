from playwright.sync_api import sync_playwright
import re

def get_avito_flats(city="Casablanca", max_price=None, min_price=None, min_surface=None):
    base_url = "https://www.avito.ma"
    search_path = f"/fr/{city.lower()}/appartements-%C3%A0_vendre"
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url + search_path)

        selector = "a.sc-1jge648-0.jZXrfL"
        page.wait_for_selector(selector)
        cards = page.query_selector_all(selector)

        for card in cards:
            try:
                title_el = card.query_selector("p[title]")
                title = title_el.inner_text().strip() if title_el else "N/A"

                price_el = card.query_selector("p.sc-1x0vz2r-0.dJAfqm")
                price = price_el.inner_text() if price_el else ""

                details_text = card.inner_text().lower()
                surface_match = re.search(r"(\d{2,4})\s?m\u00b2", details_text)
                surface = int(surface_match.group(1)) if surface_match else None

                listings.append({
                    "title": title,
                    "price": price,
                    "surface": surface,
                    "price_per_m2": round(int(re.sub(r"[^0-9]", "", price)) / surface, 2) if surface and price else None,
                    "link": base_url + card.get_attribute("href")
                })
            except Exception as e:
                continue  # Skip malformed entries

        browser.close()

    listings.sort(key=lambda x: x["price_per_m2"] or float("inf"))
    return listings


# Example usage
if __name__ == "__main__":
    flats = get_avito_flats("Casablanca", max_price=1200000, min_surface=70)
    for flat in flats:
        print(flat)
