from playwright.sync_api import Page, Playwright, expect

from Assignment.test.conftest import baseurl


def test_login_page(playwright:Playwright, baseurl):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page=  context.new_page()
    page.goto(f"{baseurl}/login")
    print(page.url)
    expect(page.locator("//h1").filter(has_text="Sign in to EventHub")).to_be_visible()
    expect(page.get_by_placeholder("you@email.com")).to_be_visible()
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()

def test_login_email(page:Page, baseurl):
    page.goto(f"{baseurl}/login")
    page.get_by_placeholder("you@email.com").fill("beginner@sample.com")
    expect(page.get_by_placeholder("you@email.com").filter(has_text="beginner@sample.com"))

def test_isolated_context(playwright:Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page= context.new_page()
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    expect(page.locator("//h1").filter(has_text="Sign in to EventHub")).to_be_visible()
    expect(page.get_by_placeholder("you@email.com")).to_be_empty()
    context.close()







