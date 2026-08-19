import time
from operator import contains

from playwright.sync_api import Page, expect


def test_end_to_end(page: Page):
    page.goto("https://eventhub.rahulshettyacademy.com")
    #login
    page.get_by_placeholder("you@email.com").fill("neha@example.com")
    page.locator("#password").fill("Test@123")
    page.get_by_role("button", name="Sign In").click()
    #Redirect to event page and click on the event
    page.locator("#nav-events").click()
    page.get_by_placeholder("Search events, venues…").fill("world")
    event_card = page.locator("#event-card").filter(has_text="World Tech Summit")
    event_card.locator("#book-now-btn").click()
    #confirm booking
    page.locator("#customerName").fill("Neha")
    page.locator("#customer-email").fill("Neha@example.com")
    page.get_by_label("Phone Number").fill("1234567890")
    page.get_by_role("button", name="Confirm Booking").click()
    # capture booking details
    event1_title = page.get_by_role("heading", name ="World Tech Summit").text_content()
    event1_booking_ref = page.locator(".booking-ref").text_content()
    event1_ticket_count = page.locator("//span[normalize-space()='1']").text_content()
    event1_total = page.locator("span.font-medium.text-gray-900").last.text_content()


    assert event1_title == "World Tech Summit"
    expect(page.locator(".booking-ref")).not_to_be_empty()
    assert event1_ticket_count == "1"

    # Browse More Events
    page.get_by_role("button", name="Browse More Events").click()
    page.get_by_placeholder("Search events, venues…").fill("Dilli")
    page.get_by_role("combobox").nth(1).select_option("Delhi")
    title2 = page.locator("#event-card").filter(has_text="Dilli Diwali Mela")
    title2.locator("#book-now-btn").click()
    page.get_by_role("button", name = "+").click()
    page.locator("#customerName").fill("Neha")
    page.locator("#customer-email").fill("neha@example.com")
    page.get_by_label("Phone Number").fill("1122334455")
    page.get_by_role("button", name="Confirm Booking").click()
    event2_title = page.get_by_role("heading", name="Dilli Diwali Mela").text_content()
    event2_booking_ref = page.locator(".booking-ref").text_content()
    event2_ticket_count = page.locator("//span[normalize-space()='2']").text_content()
    event2_total = page.locator("span.font-medium.text-gray-900").last.text_content()

    assert event1_title != event2_title
    assert event1_booking_ref != event2_booking_ref
    assert event2_ticket_count == "2"

    #My bookings
    page.locator("#nav-bookings").click()
    time.sleep(5)
    booking_card = page.locator("#booking-card")
    booking_ref = [event1_booking_ref, event2_booking_ref]

    #expect(booking_card.get_by_text("confirmed").nth(0)).to_be_visible()


    for index in range (booking_card.count()):

        expect(booking_card.get_by_text("confirmed").nth(index)).to_have_text("confirmed")

        actual_ref = booking_card.locator(".booking-ref").nth(index).inner_text()
        print(f"actual ref : {actual_ref}")
        assert actual_ref in booking_ref
        #print(page.locator(".booking-ref").nth(index).text_content())
        card = page.locator("#booking-card").nth(index)
        if page.locator(".booking-ref").nth(index).text_content() == event1_booking_ref:
            card = page.locator("#booking-card").nth(index)
            print(card.locator(".mb-1").text_content())
            assert card.locator(".mb-1").text_content() == event1_title
            assert card.get_by_text("ticket").text_content().split(" ")[1]== event1_ticket_count
            assert card.get_by_text("$").text_content() == event1_total
            card.get_by_text("View Details").click()
            assert page.locator('span.text-gray-900.font-mono').text_content() ==  event1_booking_ref
            assert page.locator(".text-2xl").text_content() == event1_title
            email = page.locator(".space-y-3").nth(1).locator(".text-right").nth(1).text_content()
            print(email)
            assert page.locator(".space-y-3").nth(2).locator(".text-right").nth(0).text_content() == event1_ticket_count
            assert page.locator(".text-lg").nth(1).text_content() == event1_total
            id = page.get_by_text("#").text_content()
            print(id)
            page.get_by_role("button", name="← Back to My Bookings").click()
        elif page.locator(".booking-ref").nth(index).text_content() == event2_booking_ref:
            print(card.locator(".mb-1").text_content())
            assert card.locator(".mb-1").text_content() == event2_title
            assert card.get_by_text("ticket").text_content().split(" ")[1] == event2_ticket_count
            assert card.get_by_text("$").text_content() == event2_total
            card.get_by_text("View Details").click()
            assert page.locator('span.text-gray-900.font-mono').text_content() == event2_booking_ref
            assert page.locator(".text-2xl").text_content() == event2_title
            email = page.locator(".space-y-3").nth(1).locator(".text-right").nth(1).text_content()
            print(email)
            assert page.locator(".space-y-3").nth(2).locator(".text-right").nth(0).text_content() == event2_ticket_count
            assert page.locator(".text-lg").nth(1).text_content() == event2_total
            id = page.get_by_text("#").text_content()
            print(id)
            assert page.locator('span.text-gray-900.font-mono').text_content() != event1_booking_ref
            page.get_by_role("button", name = "← Back to My Bookings").click()



