from django_filters import DateFromToRangeFilter, FilterSet
from rest_framework.filters import OrderingFilter

from core.choices import IdpStatuses
from core.utils import idp_status_order, task_status_order
from idp_app.models import IDP, Task


class IdpOrderingFilter(OrderingFilter):
    """Фильтр для нужного упорядочивания по полю статус."""

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if "status" in ordering:
                ordering.remove("status")
                return queryset.order_by(idp_status_order, *ordering)
            elif "-status" in ordering:
                ordering.remove("-status")
                return queryset.order_by(-idp_status_order, *ordering)

            return queryset.order_by(*ordering)

        return queryset


class IdpFilterSet(FilterSet):
    end_date = DateFromToRangeFilter(
        field_name="end_date_plan", method="filter_end_date"
    )

    class Meta:
        model = IDP
        fields = ("status", "start_date", "end_date")

    def filter_end_date(self, queryset, name, value):
        lookup_exp = "iexact"
        if value.start is not None and value.stop is not None:
            lookup_exp = "range"
            value = (value.start, value.stop)
        elif value.start is not None:
            lookup_exp = "gte"
            value = value.start
        elif value.stop is not None:
            lookup_exp = "lte"
            value = value.stop
        lookup_date_plan = "__".join([name, lookup_exp])
        lookup_date_fact = "__".join(["end_date_fact", lookup_exp])
        qs_without_closed = queryset.exclude(status=IdpStatuses.CLOSED).filter(
            **{lookup_date_plan: value}
        )
        qs_closed = queryset.filter(status=IdpStatuses.CLOSED).filter(
            **{lookup_date_fact: value}
        )
        return qs_without_closed.union(qs_closed)


class TaskOrderingFilter(OrderingFilter):
    """Фильтр для нужного упорядочивания по полю статус."""

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if "task_status" in ordering:
                ordering.remove("task_status")
                return queryset.order_by(task_status_order, *ordering)
            elif "-task_status" in ordering:
                ordering.remove("-task_status")
                return queryset.order_by(-task_status_order, *ordering)

            return queryset.order_by(*ordering)

        return queryset


class TaskFilterSet(FilterSet):
    end_date = DateFromToRangeFilter(
        field_name="task_end_date_plan", method="filter_end_date"
    )

    class Meta:
        model = Task
        fields = ("task_status", "task_start_date", "end_date")

    def filter_end_date(self, queryset, name, value):
        lookup_exp = "iexact"
        if value.start is not None and value.stop is not None:
            lookup_exp = "range"
            value = (value.start, value.stop)
        elif value.start is not None:
            lookup_exp = "gte"
            value = value.start
        elif value.stop is not None:
            lookup_exp = "lte"
            value = value.stop
        lookup_date_plan = "__".join([name, lookup_exp])
        lookup_date_fact = "__".join(["end_date_fact", lookup_exp])
        qs_without_closed = queryset.exclude(status=IdpStatuses.CLOSED).filter(
            **{lookup_date_plan: value}
        )
        qs_closed = queryset.filter(status=IdpStatuses.CLOSED).filter(
            **{lookup_date_fact: value}
        )
        return qs_without_closed.union(qs_closed)
