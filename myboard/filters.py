from django_filters import FilterSet 
from .models import Response
 
class SearchFilter(FilterSet):
    class Meta:
        model = Response
        fields = ('post',)