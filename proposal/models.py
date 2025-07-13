from django.db import models
from django.urls import reverse
from django.conf import settings
from auditlog.registry import auditlog

# Create your models here.

PROPOSAL_STATUS = (
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("clarification", "Clarification required from OO"),
    ("pending_ho", "Sent to HO"),
    ("approved_ho", "HO approved"),
)
LOB_CHOICES = (
    ("fire", "Fire"),
    ("marine_cargo", "Marine Cargo"),
    ("marine_hull", "Marine Hull"),
    ("package", "Package"),
    ("liability", "Liability"),
    ("health", "Health"),
    ("motor_od", "Motor OD"),
    ("motor_tp", "Motor TP"),
    ("personal_accident", "Personal Accident"),
    ("aviation", "Aviation"),
    ("engineering", "Engineering"),
    ("others", "Others"),
)


class Proposal(models.Model):
    office_code = models.CharField(max_length=10)
    lob = models.CharField("LOB", choices=LOB_CHOICES, max_length=20)
    segment = models.CharField(max_length=10)
    proposal_number = models.CharField(max_length=20)
    reason_for_escalation = models.TextField(help_text="Copy and paste from GC")
    format_filled = models.BooleanField(
        "Whether format is filled and sent as prescribed", max_length=10
    )
    date_of_email_sent = models.DateField("Date of email sent to RO")
    oo_remarks = models.TextField("OO Remarks")
    status = models.CharField(
        "RO Action", choices=PROPOSAL_STATUS, default="pending", max_length=20
    )
    ro_remarks = models.TextField("RO remarks")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_proposals",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)  # , blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_proposals",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.proposal_number

    def get_absolute_url(self):
        return reverse("proposal_detail", args=[str(self.pk)])


auditlog.register(Proposal)
