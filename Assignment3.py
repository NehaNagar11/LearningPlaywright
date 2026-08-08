import time

from playwright.sync_api import Page, expect
from urllib3.util import url


def test_eventHub(page:Page):
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    page.get_by_placeholder("you@email.com").fill("neha@example.com")
    page.get_by_label("password").fill("Test@123")
    page.get_by_role("button", name="Sign In").click()

    page.locator("#nav-events").click()
    expect(page.get_by_text("Upcoming Events")).to_be_visible()
    #search
    page.get_by_placeholder("Search events, venues").fill("world")
    page.get_by_role("combobox").nth(0).select_option("Conference")
    page.get_by_role("combobox").nth(1).select_option("Hyderabad")
    card = page.locator("#event-card")
    expect(card).to_have_count(1)
    title = card.get_by_role("heading").text_content()
    price= card.locator(".text-lg").text_content()
    seats = int(card.locator(".text-amber-600").text_content().split(" ")[0])
    assert title =="World Tech Summit"
    assert price.__contains__("$")
    assert seats > 0
    card.get_by_role("link", name="Book Now").click()
    assert page.get_by_role("heading", name ="World Tech Summit").text_content() == title
    priceOnCheckoutPage = page.get_by_text("$").nth(0).text_content()
    assert priceOnCheckoutPage == price
    # here I am getting old page url only, please guide me how to get new page url and verify /events/ present without using wait
    print(page.url)
    page.go_back()
    page.get_by_text("Clear filters").click()
    eventCard =  page.locator("#event-card").count()
    assert eventCard >=3
    for i in range (eventCard):
        expect(page.get_by_role("heading").nth(i)).not_to_be_empty()
        print(page.locator(".leading-snug").nth(i).text_content())
    eventTitle1 =page.locator(".leading-snug").nth(0).text_content()
    eventTitle3 =page.locator(".leading-snug").nth(2).text_content()
    assert eventTitle1 != eventTitle3








    time.sleep(5)


