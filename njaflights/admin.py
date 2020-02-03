from django.contrib import admin

from .models import Airport, NjaFlight, Passenger

# Register your models here.
class PassengerInline(admin.StackedInline):
    model = Passenger.njaflights.through
    extra = 1

class NjaFlightAdmin(admin.ModelAdmin):
    inlines = [PassengerInline]

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal =  ("njaflights",)





admin.site.register(Airport)
admin.site.register(NjaFlight, NjaFlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
