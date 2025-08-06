from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _  
from .models import Category, Product
from django.contrib.auth.models import Group

# Unregister built-in Group model
admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

    # Optional: translate list_display titles
    def get_field_queryset(self, db, db_field, request):
        return super().get_field_queryset(db, db_field, request)

    def get_changelist(self, request, **kwargs):
        changelist = super().get_changelist(request, **kwargs)
        changelist.list_display = [_(field) if isinstance(field, str) else field for field in self.list_display]
        return changelist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_available', 'category', 'image_preview')
    list_filter = ('is_available', 'category')
    search_fields = ('name',)
    ordering = ('-created_at',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = _("Image")  # Translate column title
