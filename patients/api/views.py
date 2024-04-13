from . import serializer
from patients.models import PatientCase
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters

# class CaseTypeFilter(filters.FilterSet):
#     """
#     A custom filter to filter based on case type
#     no need for this shit it can be implemented in search field
#     """
#     case_type = filters.CharFilter(lookup_expr='iexact')

#     class Meta:
#         model = PatientCase
#         fields = ['case_type']


class PatientCaseViewSet(ModelViewSet):
    serializer_class = serializer.PatientCaseSerializer
    queryset = PatientCase.objects.filter(is_accepted = True,is_approve = False)
    http_method_names = ["get",]
    search_fields = ['=diagnose']
    filter_backends = [SearchFilter]
    # filter_backends = [SearchFilter,filters.DjangoFilterBackend]
    # filterset_class = CaseTypeFilter
    # pagination_class = "PageNumberPagination"