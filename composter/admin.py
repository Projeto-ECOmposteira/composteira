from django.contrib import admin
from .models import MaterialType, Material

admin.site.register([MaterialType, Material])
