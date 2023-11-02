from django.forms import widgets
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateFilter

from .models import Ad, Category


class AdFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title contains'
    )
    create_ts = DateFilter(
        field_name='create_ts',
        lookup_expr='date__gt',
        label='Published after',
        widget=widgets.DateInput(
            attrs={
                'class': 'datepicker',
                'type': 'date'
            })
    )
    categories = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Categories',
    )

    class Meta:
        model = Ad
        fields = ['title', 'create_ts', 'categories']
