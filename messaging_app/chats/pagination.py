from rest_framework.pagination import PageNumberPagination

class customPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination.
    It sets the default page size to 20 and allows clients to override it.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: limit the maximum page size