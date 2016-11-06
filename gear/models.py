from django.db import models

class GearItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField()
    sizes = models.CharField(blank=True, default='', max_length=100, help_text='Create a new item for each size option for this item')
    inventory = models.IntegerField(default=0, help_text='Number of this item remaining')


    class Meta:
        ordering = ("name", "description")

