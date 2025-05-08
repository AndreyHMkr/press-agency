from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from press_agency.models import Redactor, Topic, Newspaper
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "years_of_experience",
        "pen_name",
        "date_of_birth",
        "autobiography",
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience", "pen_name", "date_of_birth", "autobiography")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )

@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)

@admin.register(Newspaper)
class NewspaperAdmin(ModelAdmin):
    search_fields = ("title",)
    list_filter = ("title",)
