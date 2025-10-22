from rest_framework.filters import BaseFilterBackend

class CustomBaseFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filters = {}

        for param, value in request.query_params.items():
            if param in ("page", "paging", "page_size", "ordering", "format", "search"):
                continue

            if param.endswith("__in") or param.endswith("__range"):
                filters[param] = value.split(",")
            elif param.endswith("__isnull") or value.lower() in (
                "true",
                "false",
            ):
                filters[param] = value.lower() == "true"
            else:
                filters[param] = value

        try:
            queryset = queryset.filter(**filters)
        except Exception:
            pass

        return queryset