from django.db import models

# Create your models here.
class Activity(models.Model):
    date = models.PositiveIntegerField(default=19700101)
    time = models.PositiveIntegerField(default=0)
    heart_rate = models.PositiveIntegerField(default=0)
    type = models.PositiveIntegerField(default=8)
    sleep_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.date // 10000) + "-" + str((self.date // 100) % 100) + "-" + str(self.date % 100) + " " + str(self.time // 60) + ":" + str(self.time % 60)
