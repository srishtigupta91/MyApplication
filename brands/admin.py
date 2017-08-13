from django.contrib import admin

# Register your models here.
from .models.brands import Brands
from .models.categories import Categories

admin.site.register(Brands)
admin.site.register(Categories)