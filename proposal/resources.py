from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import LineOfBusiness, ProductName


class LineOfBusinessResource(resources.ModelResource):
    class Meta:
        model = LineOfBusiness
        fields = ("id", "lob_name")  # 'id' is optional when importing


class ProductNameResource(resources.ModelResource):
    lob_name = fields.Field(
        column_name="lob_name",
        attribute="lob",
        widget=ForeignKeyWidget(LineOfBusiness, "lob_name"),
    )

    class Meta:
        model = ProductName
        fields = ("id", "product_name", "lob_name")

    #        import_id_fields = ('id',)  # Optional: if you want to match on ID

    def before_import_row(self, row, **kwargs):
        """
        Optional: create LOB on the fly if it doesn't exist.
        """
        lob_name = row.get("lob_name")
        if lob_name:
            LineOfBusiness.objects.get_or_create(lob_name=lob_name)
