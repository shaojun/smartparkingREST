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


class UserInfoAdmin(admin.ModelAdmin):
    # ...
    list_display = ('user', 'uuid', 'major_Id', 'minor_Id', 'creation_Time')


class SampleAdmin(admin.ModelAdmin):
    list_display = ('ownerBuilding', 'coordinateX', 'coordinateY', 'creation_Time')


class SampleDescriptorAdmin(admin.ModelAdmin):
    list_display = ('ownerSample',
    'uuid', 'major_Id', 'minor_Id', 'mac_address', 'tx_value', 'rssi_value', 'caculated_distance', 'creation_Time')


admin.site.register(Building, BuildingAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BeaconAround, BeaconAoundAdmin)
admin.site.register(UserInfo)
admin.site.register(Order)
admin.site.register(Sample, SampleAdmin)
admin.site.register(SampleDescriptor, SampleDescriptorAdmin)
