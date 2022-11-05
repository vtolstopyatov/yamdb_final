from django.contrib import admin
from .models import User, Comments, Review, Title, Categories, Genres
from django.contrib.auth.admin import UserAdmin


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
