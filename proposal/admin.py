from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Proposal, ProductName, LineOfBusiness
from .resources import LineOfBusinessResource, ProductNameResource

# Register your models here.
admin.site.register(Proposal)


@admin.register(LineOfBusiness)
class LineOfBusinessAdmin(ImportExportModelAdmin):
    resource_class = LineOfBusinessResource
    list_display = ("id", "lob_name")


@admin.register(ProductName)
class ProductNameAdmin(ImportExportModelAdmin):
    resource_class = ProductNameResource
    list_display = ("id", "product_name", "lob")
