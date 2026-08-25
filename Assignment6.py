import json

import time
from playwright.sync_api import Page, expect

from Assignment.test.Assignment5 import intercept_response
patched_booking = None
fakeBookingData = {
    "data": {
        "id": 132491,
        "eventId": 1,
        "userId": 36823,
        "customerName": "Neha",
        "customerEmail": "neha@example.com",
        "customerPhone": "1234567890",
        "quantity": 5,
        "totalPrice": "7500",
        "status": "confirmed",
        "bookingRef": "A-R123",
        "createdAt": "2026-08-24T11:21:18.175Z",
        "updatedAt": "2026-08-24T11:21:18.175Z",
        "event": {
            "id": 1,
            "title": "My Modified title",
            "description": "A premier technology conference bringing together 500+ industry leaders, startup founders, and engineers for two days of keynotes, workshops, and networking. Topics include AI/ML, cloud infrastructure, DevSecOps, and the future of the Indian tech ecosystem.",
            "category": "Conference",
            "venue": "Hyderabad, Hitech city",
            "city": "Hyderabad",
            "eventDate": "2026-04-18T09:00:00.000Z",
            "price": "1500",
            "totalSeats": 500,
            "availableSeats": 8,
            "imageUrl": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",
            "createdAt": "2026-02-22T23:03:37.659Z",
            "updatedAt": "2026-05-23T06:57:02.677Z"
        }
    }
}

def intercept_response(route):
    global patched_booking
    response = route.fetch()
    data = response.json()
    #print("Original data:")
    #print(data)
    original_booking_id = data['data'][0]['id']
    #print(original_booking_id)

    # Modify exactly ONE booking

    patched_booking = data["data"][0]

    patched_booking["event"]["title"] = "My Modified title"
    patched_booking["bookingRef"] = "A-R123"
    patched_booking["quantity"] = "5"
    patched_booking["totalPrice"] = "7500"
    
        # Send modified response to the browser
    route.fulfill(
        response=response,
        body=json.dumps(data),
        content_type="application/json"
    )
def intercept_response_bookingpage(route) :
    route.fulfill(
        json= fakeBookingData
    )


def test_my_booking(page: Page) :
    #page.route("**/api/bookings**",intercept_response)
    page.goto("https://eventhub.rahulshettyacademy.com")

    # login
    page.get_by_placeholder("you@email.com").fill("neha@example.com")
    page.locator("#password").fill("Test@123")
    page.get_by_role("button", name="Sign In").click()
    expect(page.locator("#nav-bookings")).to_be_visible()

    page.route(
        "**/api/bookings?page=1&limit=10",
        intercept_response
    )

    # IMPORTANT: wait specifically for the API response
    with page.expect_response(
            "**/api/bookings?page=1&limit=10"
    ) as response_info:
        page.locator("#nav-bookings").click()

    # This means the intercepted request has completed.
    response = response_info.value

    #print(">>> API status:", response.status)

    #expect(response).to_be_ok()

    page.locator("#nav-bookings").click()
    expect(page.get_by_role("heading", name ="My Bookings")).to_be_visible()
    card = page.locator("#booking-card")
    for i in range(card.count()) :
        if page.locator(".booking-ref").nth(i).text_content() ==  patched_booking["bookingRef"] :
            assert card.locator(".mb-1").nth(i).text_content() == patched_booking["event"]["title"]
            assert card.get_by_text("ticket").nth(i).text_content().split(" ")[1] == patched_booking["quantity"]
            total_price = card.get_by_text("$").nth(i).text_content()
            assert total_price.replace("$", "").replace(",", "") == patched_booking["totalPrice"]
            button_locator = card.get_by_role("link", name="View Details").nth(i).get_attribute("href")
            bookingid = button_locator.split("/")[-1]
            page.route(f"https://api.eventhub.rahulshettyacademy.com/api/bookings/{bookingid}",
                       intercept_response_bookingpage)
            card.get_by_text("View Details").nth(i).click()
            print(page.locator('span.text-gray-900.font-mono').text_content())
            assert page.get_by_text("#").text_content().replace("#","") == "132491"
            assert  page.locator('span.text-gray-900.font-mono').text_content() ==  patched_booking["bookingRef"]
            assert page.locator(".text-2xl").text_content() == patched_booking["event"]["title"]
            assert page.locator(".space-y-3").nth(2).locator(".text-right").nth(0).text_content() == patched_booking["quantity"]
            print(page.locator(".text-lg").nth(1).text_content())
            assert page.locator(".text-lg").nth(1).text_content().replace("$","").replace(",","") == patched_booking["totalPrice"]
            assert page.locator(".space-y-3").nth(1).locator(".text-right").nth(1).text_content()== "neha@example.com"
            page.get_by_role("button", name="← Back to My Bookings").click()
            for i in range(card.count()):
                if page.locator(".booking-ref").nth(i).text_content() == patched_booking["bookingRef"]:
                   assert page.locator("p.text-xl.font-bold.text-indigo-700").nth(i).text_content() == total_price
        elif page.locator(".booking-ref").nth(i).text_content() != patched_booking["bookingRef"] :
            print("Not matched with patched booking ref")
            #print(page.locator(".booking-ref").nth(i).text_content())

    time.sleep(10)