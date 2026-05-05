from django.db import models
from django.conf import settings

class DayPass(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "date"],
                name="unique_daypass_per_user_per_day"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.date} (Day Pass)"
    
class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day_pass = models.ForeignKey(DayPass, null=True, blank=True, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_checkin_per_day"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.check_in_time}"
    
