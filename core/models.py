from django.db import models


# Create your models here.
class Subscribers(models.Model):
    subscribed_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(blank=False, unique=True)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return self.name

    def _get_first_name(self):
        first_name = self.name.split()[0]
        first_name = first_name.capitalize()
        return first_name

    first_name = property(_get_first_name)

    def __unicode__(self):
        return self.first_name
