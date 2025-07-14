from django import forms
from django.urls import reverse_lazy, reverse

from .models import Proposal, LineOfBusiness, ProductName


class ProposalFormRO(forms.ModelForm):
    success_url = reverse_lazy("proposal_list")

    date_of_email_sent = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )

    reason_for_escalation = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="Copy and paste from GC",
    )
    oo_remarks = forms.CharField(
        label="OO remarks",
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    ro_remarks = forms.CharField(
        label="RO remarks",
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    class Meta:
        model = Proposal
        fields = [
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
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # ✅ Remove `user` from kwargs
        super().__init__(*args, **kwargs)

        self.fields["lob"].queryset = LineOfBusiness.objects.all().order_by("lob_name")
        self.fields["segment"].queryset = ProductName.objects.none()

        if "lob" in self.data:
            try:
                lob_id = int(self.data.get("lob"))
                self.fields["segment"].queryset = ProductName.objects.filter(
                    lob_id=lob_id
                ).order_by("product_name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["segment"].queryset = ProductName.objects.filter(
                lob=self.instance.lob
            ).order_by("product_name")

        # Add HTMX attributes for the lob field
        self.fields["lob"].widget.attrs.update(
            {
                "hx-get": reverse("ajax_load_segments"),
                "hx-target": "#id_segment",
                "hx-trigger": "change",
            }
        )


class ProposalFormOO(forms.ModelForm):
    success_url = reverse_lazy("proposal_list")

    date_of_email_sent = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )

    reason_for_escalation = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="Copy and paste from GC",
    )
    oo_remarks = forms.CharField(
        label="OO remarks",
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    class Meta:
        model = Proposal
        fields = [
            "lob",
            "segment",
            "proposal_number",
            "reason_for_escalation",
            "format_filled",
            "date_of_email_sent",
            "oo_remarks",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # ✅ Remove `user` from kwargs
        super().__init__(*args, **kwargs)
        self.fields["lob"].queryset = LineOfBusiness.objects.all().order_by("lob_name")
        self.fields["segment"].queryset = ProductName.objects.none()

        if "lob" in self.data:
            try:
                lob_id = int(self.data.get("lob"))
                self.fields["segment"].queryset = ProductName.objects.filter(
                    lob_id=lob_id
                ).order_by("product_name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["segment"].queryset = ProductName.objects.filter(
                lob=self.instance.lob
            ).order_by("product_name")

        # Add HTMX attributes for the lob field
        self.fields["lob"].widget.attrs.update(
            {
                "hx-get": reverse("ajax_load_segments"),
                "hx-target": "#id_segment",
                "hx-trigger": "change",
            }
        )

    def save(self, commit=True):
        proposal = super().save(commit=False)

        if self.user and not self.user.is_staff:
            proposal.office_code = self.user.oo_code
            if not self.user.is_staff and proposal.status == "clarification":
                proposal.status = "pending"

        if commit:
            proposal.save()

        return proposal
