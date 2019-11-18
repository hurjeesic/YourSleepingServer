from django.db import models

# Create your models here.
class Activity(models.Model):
    date = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    heartrate = models.PositiveIntegerField()
    type = models.PositiveIntegerField()

    def __str__():
        return str(date // 10000) + "-" + str((date // 100) % 100) + "-" + str(date % 100) + " " + str(time // 60) + ":" + str(time % 60)
