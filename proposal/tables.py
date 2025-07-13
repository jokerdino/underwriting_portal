# tables.py
import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from .models import Proposal


class ProposalTable(tables.Table):
    view = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = Proposal
        fields = (
            "office_code",
            "lob",
            "segment",
            "proposal_number",
            "reason_for_escalation",
            "format_filled",
            "date_of_email_sent",
            "oo_remarks",
            "status",
            "ro_remarks",
            "view",
            "edit",
        )
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-bordered table-striped table-hover",
            "id": "ProposalTable",
        }

    def render_view(self, record):
        url = reverse("proposal_detail", args=[record.pk])
        return format_html('<a class="btn btn-sm btn-info" href="{}">View</a>', url)

    def render_edit(self, record):
        url = reverse("proposal_update", args=[record.pk])
        return format_html('<a class="btn btn-sm btn-warning" href="{}">Edit</a>', url)

    def render_date_of_email_sent(self, value):
        if value:
            return format_html(
                '<span data-order="{}">{}</span>',
                value.isoformat(),
                value.strftime("%d/%m/%Y"),
            )
        return ""
