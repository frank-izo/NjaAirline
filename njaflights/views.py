from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import NjaFlight, Passenger

# Create your views here.
def index(request):
    context = {
     "njaflights": NjaFlight.objects.all()
    }
    return render(request, "njaflights/index.html", context)

def njaflight(request, njaflight_id):
    try:
        njaflight = NjaFlight.objects.get(pk=njaflight_id)
    except NjaFlight.DoesNotExist:
        raise Http404("Flight does not exist.")

    context = {
        "njaflight": njaflight,
        "passengers": njaflight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(njaflights=njaflight).all()
    }
    return render(request, "njaflights/njaflight.html", context)

def book(request, njaflight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        njaflight = NjaFlight.objects.get(pk=njaflight_id)
    except KeyError:
        return render(request, "njaflights/error.html", {"message": "No selection."})
    except NjaFlight.DoesNotExist:
        return render(request, "njaflights/error.html", {"message": "No njaflight."})
    except Passenger.DoesNotExist:
        return render(request, "njaflights/error.html", {"message": "No passenger."})

    passenger.njaflights.add(njaflight)
    return HttpResponseRedirect(reverse("njaflight", args=(njaflight_id,)))
