from django.db import models


class Card(models.Model):
    back = models.CharField(max_length=1024)
    front = models.CharField(max_length=1024)
    group = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.group} - {self.pk}"

    def serialize(self):
        return {
            "back": self.back,
            "front": self.front,
            "group": self.group,
        }


class Premium(models.Model):
    """terrible way of saving users, this is just to test if it works"""

    ip_address = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.ip_address
