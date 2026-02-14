from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def run_scraper():
    results = {}

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                    "--no-zygote",
                    "--disable-background-networking",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding"
                ]
            )

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )

            page = context.new_page()
            page.set_default_timeout(120000)

            # Load main page
            page.goto(
                "https://legalweek2026.expofp.com",
                wait_until="domcontentloaded",
                timeout=120000
            )

            # Open exhibitor list
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

    except PlaywrightTimeoutError:
        return {"error": "Navigation timeout occurred"}

    except Exception as e:
        return {"error": str(e)}

    final = []
    for name, booths in results.items():
        final.append({
            "Exhibitor Name": name,
            "Booth & Level": " , ".join(booths)
        })

    return final
