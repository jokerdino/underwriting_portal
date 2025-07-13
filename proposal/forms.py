from django import forms
from django.urls import reverse_lazy
from .models import Proposal


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

    def save(self, commit=True):
        proposal = super().save(commit=False)

        if self.user and not self.user.is_staff:
            proposal.office_code = self.user.oo_code
            if not self.user.is_staff and proposal.status == "clarification":
                proposal.status = "pending"

        if commit:
            proposal.save()

        return proposal
