from django.contrib import admin
from .models import Item

"""
   Customizes the administration interface for the Item model.
   This class registers the Item model with the admin site and provides a custom
   display format for the model's fields in the admin panel.
   """

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
