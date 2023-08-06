from django.db import models


class Platform(models.TextChoices):
    ios = "ios", "Ios"
    android = "android", "Android"


class PurchaseResponseStatus(models.TextChoices):
    ok = "ok"
    error = "error"
