"""Tag ViewSet and Serializers"""
from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from whattodoapi.models import Tags

class TagViewSet(ViewSet):
    """Tag view set"""

    def list(self,request):
        """GET all tag object"""
        app_user = User.objects.get(id=request.auth.user.id)

        tags = Tags.objects.filter(author=app_user)
        serialized_Tags = TagSerializer(tags, many=True)
        return Response(serialized_Tags.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handles get requests for a single tag"""
        try:
            tag = Tags.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def create(self, request):
        """Handle POST requests for tags"""
        app_user = User.objects.get(id=request.auth.user.id)
        tag = Tags()
        tag.label = request.data["label"]
        tag.author = app_user
        
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Handle PUT requests for tags"""
        try:
            tag = Tags.objects.get(pk=pk)
        except Tags.DoesNotExist:
            return Response({'message':'tag not found'}, status=status.HTTP_404_NOT_FOUND)
        tag.label = request.data["label"]
        tag.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for tags"""
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
        fields = ('id', 'label', 'author')