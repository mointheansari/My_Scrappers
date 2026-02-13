from playwright.sync_api import sync_playwright

def run_scraper():
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto("https://legalweek2026.expofp.com")
        page.wait_for_selector(".icon-search")
        page.click(".icon-search")
        page.wait_for_selector(".efp-overlay__scroll")
        page.wait_for_selector(".efp-entity-item")

        sidebar = page.locator(".efp-overlay__scroll").first
        no_new = 0

        while no_new < 6:
            cards = page.locator(".efp-entity-item")
            before = len(results)

            for i in range(cards.count()):
                card = cards.nth(i)
                name_el = card.locator(".efp-entity-item__title")
                if not name_el.count():
                    continue

                name = name_el.inner_text().strip()

                if name not in results:
                    results[name] = []

                details = card.locator(".efp-entity-item__details-item")
                for j in range(details.count()):
                    text = details.nth(j).inner_text().strip()
                    text = " ".join(text.split())
                    if text and text not in results[name]:
                        results[name].append(text)

            if len(results) == before:
                no_new += 1
            else:
                no_new = 0

            sidebar.evaluate("el => el.scrollBy(0, 600)")
            page.wait_for_timeout(300)

        browser.close()

    final = []
    for name, booths in results.items():
        final.append({
            "Exhibitor Name": name,
            "Booth & Level": " , ".join(booths)
        })

    return final
