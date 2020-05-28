from rest_framework.pagination import PageNumberPagination

class OrderPageNumberPagination(PageNumberPagination):
    page_size = 5