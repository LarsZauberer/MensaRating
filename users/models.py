from django.db import models

# Create your models here.
class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    attributes = models.TextField(default="")
    uses = models.IntegerField(default=1)
