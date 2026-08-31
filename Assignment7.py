from playwright.sync_api import expect, Playwright

from Assignment.test.utils.apiBase import ApiUtils


def test_end_to_end(playwright: Playwright):
    api_utils = ApiUtils()
    token = api_utils.get_token(playwright)
    reference_code, title, quantity, total_price, customerEmail, eventId, id= api_utils.create_booking(playwright)
    browser = playwright.chromium.launch(headless=False)
    context =  browser.new_context()
    page = context.new_page()
    page.add_init_script(f"""localStorage.setItem('eventhub_token','{token}')""")
    page.goto("https://eventhub.rahulshettyacademy.com")
    page.locator("#nav-bookings").click()
    page.wait_for_url("https://eventhub.rahulshettyacademy.com/bookings")
    card = page.locator("#booking-card")
    expect(card.first).to_be_visible()
    for i in range(card.count()):
        if page.locator(".booking-ref").nth(i).text_content() == reference_code :
            assert card.locator(".mb-1").nth(i).text_content() == title
            assert int(card.get_by_text("ticket").nth(i).text_content().split(" ")[1]) == quantity
            card.get_by_text("View Details").nth(i).click()
            assert page.locator('span.text-gray-900.font-mono').text_content() == reference_code
            assert page.locator(".text-2xl").text_content() == title
            assert int(page.locator(".space-y-3").nth(2).locator(".text-right").nth(0).text_content()) == quantity
            assert page.locator(".text-lg").nth(1).text_content().replace("$", "").replace(",", "") == total_price
            assert page.locator(".space-y-3").nth(1).locator(".text-right").nth(1).text_content() == customerEmail
            break
    api_utils.cancel_booking(playwright, reference_code, id)
    page.goto("https://eventhub.rahulshettyacademy.com/bookings")
    expect(page.get_by_text("No bookings yet")).to_be_visible()
