from django.contrib.auth.models import Group
from django.db import models


# Create your models here.
class Events(models.Model):

    title = models.CharField(verbose_name="News Title", max_length=255)
    description = models.TextField(verbose_name="Descriptions")
    usergroups = models.ManyToManyField(Group, related_name='groups',)
    publish_date = models.DateField(verbose_name="Select publish date")
    deals = models.ForeignKey('deals.Deals', related_name='event_deals')
    upload_image = models.ImageField(upload_to='media/', blank=True, null=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def get_usergroups(self):
        return " \n ".join([str(user) for user in self.group.all()])