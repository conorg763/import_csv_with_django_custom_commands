from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "variant", "year"]
    list_filter = ["make"]
    search_fields = ["make","model"]
# Register your models here.
