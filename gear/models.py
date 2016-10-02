from django.db import models

class GearItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField()
    #quantity = models.IntegerField(choices=[0,1,2,3,4,5,6,7,8,9], default=0)
    #sizes = models.CharField(choices=['small, medium, large'])

    class Meta:
        ordering = ("name", "description")

