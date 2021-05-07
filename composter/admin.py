from django.contrib import admin
from .models import MaterialType, Material, Composter

admin.site.register([MaterialType, Material, Composter])
