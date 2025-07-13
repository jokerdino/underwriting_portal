# from django.shortcuts import render
from django.db.models import Count

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

# from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2.views import SingleTableView

# from django_filters.views import FilterView

from .models import Proposal
from .forms import ProposalFormRO, ProposalFormOO
from .tables import ProposalTable

# from .filters import ProposalFilter
# Create your views here.


class ProposalListView(LoginRequiredMixin, SingleTableView):  ##Mixin, FilterView):
    model = Proposal
    table_class = ProposalTable
    template_name = "proposal/list.html"
    # filterset_class = ProposalFilter

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Office filter for non-staff
        if not user.is_staff:
            qs = qs.filter(office_code=user.oo_code)

        # ✅ New: get status from URL kwarg
        status = self.kwargs.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["status"] = self.kwargs.get("status", "All")
    #     # counts = qs.values("status").annotate(count=Count("id")).order_by("status")

    #     # context["status_counts"] = counts

    #     # return context
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ Add status counts for the table
        qs = self.model.objects.all()
        user = self.request.user
        if not user.is_staff:
            qs = qs.filter(office_code=user.oo_code)

        counts = qs.values("status").annotate(count=Count("id")).order_by("status")

        context["status_counts"] = counts

        return context


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal

    template_name = "proposal/form.html"
    success_url = reverse_lazy("proposal_list_by_status", kwargs={"status": "pending"})

    def get_form_class(self):
        if self.request.user.is_staff:
            return ProposalFormRO
        else:
            return ProposalFormOO

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user  # Both at creation
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pass user for NonStaff form
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new proposal"
        return context


class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = Proposal

    template_name = "proposal/form.html"
    success_url = reverse_lazy("proposal_list_by_status", kwargs={"status": "pending"})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit proposal"
        return context

    def get_form_class(self):
        if self.request.user.is_staff:
            return ProposalFormRO
        else:
            return ProposalFormOO

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pass user for NonStaff form
        return kwargs

    def form_valid(self, form):
        form.instance.updated_by = self.request.user  # Only update this
        return super().form_valid(form)


class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = "proposal/detail.html"
