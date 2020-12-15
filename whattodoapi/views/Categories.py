"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http.response import HttpResponseServerError
from whattodoapi.models import Categories

class CategoryViewSet(ViewSet):
    """Categories view set"""

    def list(self,request):
        """GET a new Categories object"""
        categories = Categories.objects.all()
        serialized_categories = CategoriesSerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Categories
        fields = ('id', 'label')