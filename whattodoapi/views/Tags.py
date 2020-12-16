"""Tag ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http.response import HttpResponseServerError
from whattodoapi.models import Tags

class TagViewSet(ViewSet):
    """Tag view set"""

    def list(self,request):
        """GET all tag objecta"""
        Tag = Tags.objects.all()
        serialized_Tag = TagSerializer(Tag, many=True)
        return Response(serialized_Tag.data, status=status.HTTP_200_OK)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tag"""
    class Meta:
        model = Tags
        fields = ('id', 'label')