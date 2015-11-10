from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User
import uuid
import datetime


class Building(models.Model):
    mapUrl = models.CharField(max_length=300, null=True, blank=True, help_text='map url for this building.')
    latitude = models.CharField(default='0', max_length=60, help_text='latitude for this building')
    longitude = models.CharField(default='0', max_length=60, help_text='longitude for this building')
    description = models.TextField(blank=True, default="",
                                   help_text='additional description for this building, where it located, name and etc.')
    creationTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Building with pk: " + str(self.pk)


class Board(models.Model):
    ownerBuilding = models.ForeignKey(Building, related_name='boards')
    isCovered = models.BooleanField("If obstacle sensor covered by sth, the value will be True, otherwise False")
    # isLocked = models.BooleanField("If obstacle sensor covered by sth, the value is True, otherwise False")
    coordinateX = models.IntegerField(default=0, help_text='X coordinate for this board located in a building')
    coordinateY = models.IntegerField(default=0, help_text='Y coordinate for this board located in a building')
    description = models.TextField(blank=True, default="",
                                   help_text='additional description for this board, will show in mobile device')
    boardIdentity = models.TextField(primary_key=True, max_length=80,
                                     help_text='An unique identity value to identity a board, like the board Mac and etc.')
    command = models.TextField(blank=True, default="",
                               help_text='A pre-defined command text which should be read and executed by board')

    def __str__(self):
        if self.isCovered:
            return "board: " + str(self.pk) + " (occupied), with X-Y coor:" + str(self.coordinateX) + "-" + str(
                self.coordinateY) + ", " + str(self.description)
        else:
            return "board: " + str(self.pk) + " (no occupied), with X-Y: " + str(self.coordinateX) + "-" + str(
                self.coordinateY) + ", " + str(self.description)


class BeaconAround(models.Model):
    ownerBoard = models.ForeignKey(Board)
    uuid = models.CharField(max_length=40)
    major_Id = models.CharField(max_length=20)
    minor_Id = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=40)
    tx_value = models.IntegerField(default=0)
    rssi_value = models.IntegerField(default=0)
    caculated_distance = models.FloatField()
    updated_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "uuid: " + self.uuid + "|" + self.major_Id + "|" + self.minor_Id + ", rssi: " + str(
            self.rssi_value) + ", dis(meter): " + str(self.caculated_distance)

    def ownedbyboardstr(self):
        return str(self.ownerBoard)

    ownedbyboardstr.short_description = "Owned by board"

    def since_last_refresh_due(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if self.updated_time:
            timediff = now - self.updated_time
            return timediff.total_seconds()
        else:
            return -1

    since_last_refresh_due.short_description = "last Refresh due(s)"


class UserInfo(models.Model):
    user = models.ForeignKey(User, related_name='parkingUser')
    uuid = models.CharField(max_length=40)
    major_Id = models.CharField(max_length=20)
    minor_Id = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=40)
    creation_Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " (registered with uuid: " + self.uuid + "|" + self.major_Id + "|" + self.minor_Id + ")"


class Order(models.Model):
    owner = models.ForeignKey(UserInfo, related_name='orders')
    to_Board = models.ForeignKey(Board, related_name='orderDetail')
    creation_Time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)

    def __str__(self):
        return "order is on board:'" + str(
            self.to_Board) + "' by users: '" + str(self.owner) + "' at: '" + str(
            self.creation_Time) + "', now status: '" + self.status + "'"

    def ownedbyuserstr(self):
        return str(self.owner)

    ownedbyuserstr.short_description = "Put by"


class Sample(models.Model):
    ownerBuilding = models.ForeignKey(Building)
    coordinateX = models.IntegerField(default=0, help_text='X coordinate for this sampling point located in a building')
    coordinateY = models.IntegerField(default=0, help_text='Y coordinate for this sampling point located in a building')
    # sampleSignalDescriptors = models.CharField(max_length=200)
    creation_Time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="", help_text='additional description for this sample point.')

    class Meta:
        unique_together = ('ownerBuilding', 'coordinateX', 'coordinateY')

    def __str__(self):
        return "Sample for building " + str(self.ownerBuilding)


class SampleDescriptor(models.Model):
    ownerSample = models.ForeignKey(Sample, related_name='sampleDescriptors')
    uuid = models.CharField(max_length=40)
    major_Id = models.CharField(max_length=20)
    minor_Id = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=40)
    tx_value = models.IntegerField(default=0)
    rssi_value = models.IntegerField(default=0)
    caculated_distance = models.FloatField()
    creation_Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "uuid: " + self.uuid + "|" + self.major_Id + "|" + self.minor_Id + ", rssi: " + str(
            self.rssi_value) + ", dis(meter): " + str(self.caculated_distance)


# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='uploadedmaps/%m/%d')
    # 100 px equal how many real life meters, like say the value is 5, means
    # 100px in bitmap equal 5meters, default set to 2.
    # mapscale = models.FloatField(default=2)
