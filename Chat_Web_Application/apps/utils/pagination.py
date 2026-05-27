from rest_framework.pagination import PageNumberPagination
from apps.utils.api_response import api_response
from rest_framework.exceptions import NotFound

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override to handle invalid page numbers gracefully
        """
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            raise NotFound(detail="Invalid page number")

    def get_paginated_response(self, data):
        page = self.page
        paginator = page.paginator

        return api_response(
            success=True,
            message="Data retrieved successfully",
            data={
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page.number,
                "page_size": self.get_page_size(self.request),
                "has_next": page.has_next(),
                "has_previous": page.has_previous(),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
            status_code=200
        )
        