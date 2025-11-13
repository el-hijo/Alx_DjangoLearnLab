
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
    search_fields = ('title','author')
    list_filter = ('publication_year',)
    
admin.site.register(Book, BookAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add your custom fields to admin forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_photo')}),
    )

# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)
