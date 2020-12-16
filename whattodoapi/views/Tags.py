"""Tag ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.exceptions import ValidationError

from whattodoapi.models import Tags

class TagViewSet(ViewSet):
    """Tag view set"""

    def list(self,request):
        """GET all tag object"""
        Tag = Tags.objects.all()
        serialized_Tag = TagSerializer(Tag, many=True)
        return Response(serialized_Tag.data, status=status.HTTP_200_OK)

    def create(self, request):
        """ """
        tag = Tags()
        tag.label = request.data["label"]
        
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """"""

    def destroy(self, request, pk=None):
        """"""
        try:
            tag = Tags.objects.get(pk=pk)
            tag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist as ex:
            return Response({'message': ex.args[0]})
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tag"""
    class Meta:
        model = Tags
        fields = ('id', 'label')