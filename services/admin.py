from django.contrib import admin

from .models import *

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('mapUrl', 'description', 'creationTime')


class BeaconAoundInline(admin.TabularInline):
    model = BeaconAround
    extra = 2

class BoardAdmin(admin.ModelAdmin):
    inlines = [BeaconAoundInline]

class BeaconAoundAdmin(admin.ModelAdmin):
    # ...
    list_display = (
        'ownedbyboardstr', 'uuid', 'major_Id', 'minor_Id', 'rssi_value', 'caculated_distance', 'since_last_refresh_due')


class OrderAdmin(admin.ModelAdmin):
    # ...
    list_display = ('ownedbyuserstr', 'to_Board', 'creation_Time', 'status')


class UserAdmin(admin.ModelAdmin):
    # ...
    list_display = ('user_Name', 'uuid', 'major_Id', 'minor_Id', 'creation_Time')


admin.site.register(Building, BuildingAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BeaconAround, BeaconAoundAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
