from enum import Enum

from django.core import serializers
from django.db.models import Q, Avg
from django.db.models.functions import Coalesce
from django.forms import FloatField
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.contrib.postgres.aggregates import ArrayAgg

from movies import models
from movies.models import Filmwork


class RoleType(Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'


class MoviesApiMixin(View):
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def _filter_and_aggregate_roles(role: RoleType) -> ArrayAgg:
        return ArrayAgg(
            'persons__full_name',
            distinct=True,
            filter=Q(personfilmwork__role=role.value)
        )

    def get_queryset(self):
        return super().get_queryset(
        ).prefetch_related(
            'genres',
            'persons',
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'type',
        ).annotate(
            rating=Coalesce(Avg('rating'), 0.0),
            genres=ArrayAgg('genres__name', distinct=True, filter=Q(genres__name__isnull=False)),
            actors=self._filter_and_aggregate_roles(RoleType.ACTOR),
            directors=self._filter_and_aggregate_roles(RoleType.DIRECTOR),
            writers=self._filter_and_aggregate_roles(RoleType.WRITER),
        ).order_by('title')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    http_method_names = ('get',)
    paginate_by = 50
    model = models.Filmwork

    def get(self, request, *args, **kwargs):
        movies_qs = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            movies_qs,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(movies_qs),
        }
        return self.render_to_response(context)


class MovieDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return {**kwargs['object']}

