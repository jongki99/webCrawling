from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.naver.com")
page.screenshot(path="./temp/screenshot.png")

"""
try:
    p = sync_playwright().start()
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://google.com")
    page.screenshot(path="screenshot.png")
except Exception as e:
    print(f"An error occurred: {e}")

"""
