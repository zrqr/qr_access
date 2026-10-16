"""Runs a Playwright browser and pushes a screenshot to the relay every few seconds.

Environment:
  RELAY_URL    e.g. https://viewer.example.com   (the EC2 relay)
  PUSH_SECRET  must match the relay's PUSH_SECRET
  START_URL    page to open first (optional)
"""

import asyncio
import os
import urllib.request

from playwright.async_api import async_playwright

RELAY_URL = os.environ["RELAY_URL"].rstrip("/")
PUSH_SECRET = os.environ["PUSH_SECRET"]
START_URL = os.environ.get("START_URL", "https://example.com")
INTERVAL = float(os.environ.get("FRAME_SECONDS", "2"))
CHROMIUM = os.environ.get("CHROMIUM_PATH")  # optional: use a specific Chromium binary


def push(png: bytes) -> None:
    request = urllib.request.Request(
        f"{RELAY_URL}/push",
        data=png,
        method="POST",
        headers={"Content-Type": "image/png", "X-Push-Secret": PUSH_SECRET},
    )
    with urllib.request.urlopen(request, timeout=10):
        pass


async def main() -> None:
    async with async_playwright() as p:
        launch = {"args": ["--no-sandbox"]}
        if CHROMIUM:
            launch["executable_path"] = CHROMIUM
        browser = await p.chromium.launch(**launch)
        page = await browser.new_page(viewport={"width": 1100, "height": 700})
        await page.goto(START_URL, timeout=30000)
        while True:
            try:
                await asyncio.to_thread(push, await page.screenshot(type="png"))
            except Exception as error:  # keep streaming through transient errors
                print(f"frame failed: {error}", flush=True)
            await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
