import pytest
from playwright.sync_api import Page, Playwright, expect

from Assignment.test.conftest import baseurl


def test_basicSetup(playwright : Playwright, baseurl ):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page=  context.new_page()
    print(f"{baseurl}/login")
    expect(page.goto(f"{baseurl}/login")).to_have_url("https://eventhub.rahulshettyacademy.com/login")
    expect(page.get_by_role("heading")).to_contain_text("EventHub")
    expect(page.get_by_placeholder("you@email.com")).to_be_visible()
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()
    page.get_by_placeholder("you@email.com").fill("beginner@sample.com")

    context = browser.new_context()
    page=context.new_page()
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    expect(page.get_by_role("heading", name="ign in to EventHub")).to_be_visible()
    expect(page.get_by_placeholder("you@email.com")).to_be_empty()







