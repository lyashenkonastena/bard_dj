from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import AdFilter
from .forms import AdForm, ReplyForm
from .models import Ad, Reply


class AdList(ListView):
    model = Ad
    ordering = '-create_ts'
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('personal'):
            queryset = queryset.filter(user=self.request.user)
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = self.kwargs['personal']
        context['filterset'] = self.filterset
        return context


class AdDetail(DetailView):
    model = Ad
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad'


class AdCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_ad',)
    form_class = AdForm
    model = Ad
    template_name = 'board/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'New'
        context['object_type'] = 'ad'
        return context

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        ad.save()
        return super().form_valid(form)


class AdEdit(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('board.change_ad',)
    form_class = AdForm
    model = Ad
    template_name = 'board/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Change'
        context['object_type'] = 'ad'
        return context

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = ('board.delete_ad',)
    model = Ad
    template_name = 'board/delete.html'
    success_url = reverse_lazy('ad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'ad'
        return context

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class ReplyDetail(DetailView):
    model = Reply
    template_name = 'board/reply_detail.html'
    context_object_name = 'reply'


class ReplyCreate(PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = ('board.add_reply',)
    form_class = ReplyForm
    model = Reply
    template_name = 'board/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'New'
        context['object_type'] = 'reply'
        context['ad'] = Ad.objects.get(id=self.kwargs['ad_pk'])
        return context

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.ad = Ad.objects.get(id=self.kwargs['ad_pk'])
        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ad_details', kwargs={'pk': self.kwargs['ad_pk']})

    def test_func(self):
        ad = Ad.objects.get(id=self.kwargs['ad_pk'])
        return ad.user != self.request.user


class ReplyEdit(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('board.change_reply',)
    form_class = ReplyForm
    model = Reply
    template_name = 'board/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Change'
        context['object_type'] = 'reply'
        context['ad'] = self.object.ad
        return context

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.save()
        return super().form_valid(form)

    def test_func(self):
        reply = self.get_object()
        return reply.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('ad_details', kwargs={'pk': self.object.ad.pk})


class ReplyDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = ('board.delete_reply',)
    model = Reply
    template_name = 'board/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'reply'
        return context

    def test_func(self):
        reply = self.get_object()
        return reply.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('ad_details', kwargs={'pk': self.object.ad.pk})


class ReplyAcceptDecline(PermissionRequiredMixin, UserPassesTestMixin, View):
    permission_required = ('board.change_reply',)

    def get(self, *args, **kwargs):
        reply = Reply.objects.get(id=kwargs['pk'])
        if self.request.get_full_path() == reverse('reply_decline', kwargs=kwargs):
            reply.accepted = False
            reply.declined = True
        else:
            reply.accepted = True
            reply.declined = False
        reply.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def test_func(self):
        reply = Reply.objects.get(id=self.kwargs['pk'])
        return reply.ad.user == self.request.user
