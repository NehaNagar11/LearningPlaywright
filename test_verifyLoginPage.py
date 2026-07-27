import time

from playwright.sync_api import Page, expect


def test_eventhub(page:Page) :
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    inputlocator = page.get_by_label("Email").get_attribute("placeholder")
    print(inputlocator)
    assert inputlocator == "you@email.com"
    button = page.get_by_role("button")
    expect(button).to_have_text('Sign In')


def test_simpleloginpage(page:Page) :
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    if page.get_by_label("Password").is_visible():
        print("Password is visible")
    currenturl = page.url
    logincheck = currenturl.__contains__("login")
    assert logincheck
    heading = page.get_by_role("heading", name="Sign in to EventHub").is_visible()
    assert heading


