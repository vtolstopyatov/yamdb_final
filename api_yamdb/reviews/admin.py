from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Categories, Comments, Genres, Review, Title, User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Title)
admin.site.register(Genres)
admin.site.register(Categories)
