from django.db import models


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class Status(models.TextChoices):
    APPROVED = "approved", "Approved"
    INACTIVE = "inactive", "Inactive"


class Account(models.TextChoices):
    NORMAL = "normal", "Normal"
    PREMIUM = "premium", "Premium"
