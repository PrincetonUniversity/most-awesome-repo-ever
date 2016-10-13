from django.db import models

class GearItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField()
    sizes = models.CharField(blank=True, default='', max_length=100, help_text='use abbreviations and separate with spaces (ex: xs s m l xl)')
    custom_text = models.IntegerField(blank=True, default=0, help_text='max number of characters (0 if no custom text allowed)')


    class Meta:
        ordering = ("name", "description")

