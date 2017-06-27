from django.contrib import admin

# Register your models here.

from .models import Brands, Categories

# Register your models here.

admin.site.register(Brands)
admin.site.register(Categories)