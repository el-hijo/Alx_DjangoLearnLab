
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

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Optional: if you have extra fields, add them here
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('profile_photo',)}),  # example
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('profile_photo',)}),
    )
