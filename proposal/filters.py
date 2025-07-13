from django_filters import FilterSet
from .models import Proposal


class ProposalFilter(FilterSet):
    class Meta:
        model = Proposal
        fields = {
            "office_code": ["exact", "contains"],
            "proposal_number": ["exact"],
            "ro_action": ["exact"],
        }
