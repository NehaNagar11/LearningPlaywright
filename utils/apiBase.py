from email import header

from playwright.sync_api import Playwright, expect


class ApiUtils :

    def get_token(self, playwright : Playwright):
        user_email="neha@example.com"
        user_password="Test@123"
        api_context_request = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_context_request.post("/api/auth/login", data={"email": user_email, "password": user_password})
        assert response.ok
        responseToken =  response.json()
        token =responseToken['token']
        return token

    def get_events(self, playwright : Playwright):
        token = self.get_token(playwright)
        api_context_request = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_context_request.get("/api/events", headers={"authorization" : f"Bearer {token}", "content-type" : "application/json"})
        events = response.json()
        assert response.ok
        for i in range(0,len(events)):
            availableseats = events['data'][i]['availableSeats']
            if availableseats >=2 :
                 id=  events['data'][i]['id']
                 title=   events['data'][i]['title']
                 category=   events['data'][i] ['category']
                 city=   events['data'][i]['city']
                 price =  events['data'][i]['price']
                 break
        return id

    def create_booking(self, playwright: Playwright):
        event_id =self.get_events(playwright)
        token= self.get_token(playwright)
        api_context_request = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        create_response = api_context_request.post("/api/bookings",
                   data={"eventId": event_id, "customerName": "Priya Sharma",  "customerEmail": "priya.sharma@email.com","customerPhone": "9876543210","quantity": 2},
                   headers= {"authorization" : f"Bearer {token}",
                                           "content-type": "application/json"})
        assert create_response.ok
        booking_data = create_response.json()
        id = booking_data['data']['id']
        eventId = booking_data['data']['eventId']
        reference_code = booking_data['data']['bookingRef']
        total_price = booking_data['data']['totalPrice']
        title = booking_data['data']['event']['title']
        price = booking_data['data']['event']['price']
        quantity = booking_data['data']['quantity']
        customerEmail = booking_data['data']['customerEmail']
        lookup_response = api_context_request.get(f"/api/bookings/ref/{reference_code}",
                                                   headers= {"authorization" : f"Bearer {token}",
                                                   "content-type": "application/json"})
        assert lookup_response.ok
        lookup_response = lookup_response.json()

        assert lookup_response["data"]["id"] ==     id
        assert lookup_response["data"]["bookingRef"] == reference_code
        assert lookup_response['data']['event']['title']    == title
        assert lookup_response['data']['totalPrice'] == total_price
        assert lookup_response['data']['event']['price'] == price
        return reference_code, title, quantity, total_price, customerEmail, eventId, id

    def cancel_booking(self,playwright: Playwright, reference_code, id):
        token = self.get_token(playwright)
        api_context_request = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        try :
            response = api_context_request.delete(f"/api/bookings/{id}",headers= {"authorization" : f"Bearer {token}"})
            assert response.ok
            lookup_response = api_context_request.get(f"/api/bookings/ref/{reference_code}",
                                                      headers={"authorization": f"Bearer {token}",
                                                               "content-type": "application/json"})
            lookup_response = lookup_response.json()
            assert lookup_response['error'] == f'Booking with reference "{reference_code}" not found'
        finally:
            api_context_request.dispose()
