from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15
    min_page_size = 5

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        if page_size is not None and page_size < self.min_page_size:
            return self.min_page_size
        return page_size
