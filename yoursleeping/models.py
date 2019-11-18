from django.db import models

# Create your models here.
class Activity(models.Model):
    date = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    heartrate = models.PositiveIntegerField()
    type = models.PositiveIntegerField()

    def __str__(self):
        return str(self.date // 10000) + "-" + str((self.date // 100) % 100) + "-" + str(self.date % 100) + " " + str(self.time // 60) + ":" + str(self.time % 60)
