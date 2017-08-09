from django.db import models

# Create your models here.
from model_utils import FieldTracker
from model_utils.fields import StatusField, MonitorField, SplitField
from model_utils import Choices
from model_utils.managers import QueryManager


class Article(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS = Choices(
        (DRAFT, 'draft'),
        (PUBLISHED, 'published')
    )
    status_changed = MonitorField(monitor='status')
    is_removed = models.BooleanField(default=False)
    published_at = MonitorField(monitor='status', when=['published'])
    title = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20)
    body = SplitField()




class Post(models.Model):
    published = models.BooleanField()
    pub_date = models.DateField()
    objects = models.Manager()
    public = QueryManager(published=True).order_by('-pub_date')
    title = models.CharField(max_length=100)
    body = models.TextField()
    tracker = FieldTracker()