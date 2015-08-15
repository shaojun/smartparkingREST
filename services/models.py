from django.db import models
from django.utils.timezone import utc
import datetime


class Building(models.Model):
    mapUrl = models.CharField(max_length=300, null=True, help_text='map url for this building.')
    description = models.TextField(null=True,
                                   help_text='additional description for this building')
    creationTime = models.DateTimeField(auto_now_add=True)


class Board(models.Model):
    ownerBuilding = models.ForeignKey(Building)
    isCovered = models.BooleanField("If obstacle sensor covered by sth, the value is True, otherwise False")
    #isLocked = models.BooleanField("If obstacle sensor covered by sth, the value is True, otherwise False")
    coordinateX = models.IntegerField(default=0, help_text='X coordinate for this board located in a building')
    coordinateY = models.IntegerField(default=0, help_text='Y coordinate for this board located in a building')
    description = models.TextField(null=True,
                                   help_text='additional description for this board, will show in mobile device')
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


class User(models.Model):
    user_Name = models.CharField(max_length=200, unique=True)
    uuid = models.CharField(max_length=40)
    major_Id = models.CharField(max_length=20)
    minor_Id = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=40)
    creation_Time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_Name + " (registered with uuid: " + self.uuid + "|" + self.major_Id + "|" + self.minor_Id + ")"


class Order(models.Model):
    by_User = models.ForeignKey(User)
    to_Board = models.ForeignKey(Board)
    creation_Time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)

    def __str__(self):
        return "order is on board:'" + str(
            self.to_Board.board_Id) + "' by users: '" + self.by_User.user_Name + "' at: '" + str(
            self.creation_Time) + "', now status: '" + self.status + "'"

    def ownedbyuserstr(self):
        return str(self.by_User)

    ownedbyuserstr.short_description = "Put by"
