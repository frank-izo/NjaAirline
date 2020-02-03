from django.db.models import Max
from django.test import Client, TestCase
from .models import Airport,NjaFlight, Passenger

# Create your tests here.
class NjaFlightsTestCase(TestCase):
    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="city A")
        a2 = Airport.objects.create(code="BBB", city="city B")

        # Create njaflights.
        NjaFlight.objects.create(origin=a1, destination=a2, duration=100)
        NjaFlight.objects.create(origin=a1, destination=a1, duration=200)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 2)

    def  test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_njaflight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = NjaFlight.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_njaflight())

    def test_invalid_njaflight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = NjaFlight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_njaflight())

    def test_invalid_njaflight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = NjaFlight.objects.get(origin=a1, destination=a2)
        f.duration = -100
        self.assertFalse(f.is_valid_njaflight())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["njaflights"].count(), 2)

    def _test_valid_njaflight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = NjaFlight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_njaflight_page(self):
        max_id = NjaFlight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_njaflight_page_passengers(self):
        f = NjaFlight.objects.get(pk=1)
        p = Passenger.objects.create(first="nam", last="memberr")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_njaflight_page_non_passengers(self):
        f = NjaFlight.objects.get(pk=1)
        p = Passenger.objects.create(first="nam", last="memberr")

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
