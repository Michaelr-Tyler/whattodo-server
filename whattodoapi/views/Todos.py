"""Category ViewSet and Serializers"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from whattodoapi.models import Todos, Tags, Categories, TodoTags
from django.contrib.auth.models import User
from rest_framework.response import Response



class TodoViewSet(ViewSet):
    """Todo view set"""
    def create(self, request):
        """Handle Post Operations
        returns -- JSON Serialized todo instance
        """
        app_user = User.objects.get(id=request.auth.user.id )
        todo = Todos()
        todo.user = app_user    
        todo.urgent = request.data["urgent"]
        todo.important = request.data["important"]
        

    #assign category based on the responses important and urgent rankings
        if request.data["urgent"] >= 5 and request.data["important"] >= 5:
            todo.category = Categories.objects.get(pk=1)
        elif request.data["urgent"] < 5 and request.data["important"] >= 5:
            todo.category = Categories.objects.get(pk=2)
        elif request.data["urgent"] >= 5 and request.data["important"] < 5:
            todo.category = Categories.objects.get(pk=3)
        elif request.data["urgent"] < 5 and request.data["important"] < 5:
            todo.category = Categories.objects.get(pk=4)
        todo.task = request.data["task"]

    #now its time for them todotags
    #first lets get any tag ids from the request, this should be an array
        tag_ids = request.data["tagIds"]
    #next loop through the tags and match em up
        try:
            tags = [Tags.objects.get(pk=tag_id) for tag_id in tag_ids]
        except Tags.DoesNotExist:
                return Response({'message': 'request contains a tagId for a non-existent tag'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    #after that save that todo
        try: 
            todo.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    #now we need to save the todotags
        for tag in tags:
            todo_tag = TodoTags(todo=todo, tag=tag)
            todo_tag.save()
        
        serializer = TodoSerializer(todo, context={'request': request})
        return Response(serializer.data)

    def list(self,request):
        """GET a new Todo object"""
        todos = Todos.objects.all()
        serialized_todos = TodoSerializer(todos, many=True, context={'request': request})
        return Response(serialized_todos.data, status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for User"""
    full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = User
        fields= ('id', 'full_name')
        
class TodoTagsSerializer(serializers.ModelSerializer):
    """JSON serializer for Todo Tags"""
    class Meta:
        model = Tags
        fields = ('id', 'label')

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for Categories"""
    class Meta:
        model = Categories
        fields = ('id', 'label')

class TodoSerializer(serializers.ModelSerializer):
    """JSON serializer for Todo"""
    user = UserSerializer(many=False)
    category = CategoriesSerializer(many=False)
    tags = TodoTagsSerializer(many=True)

    class Meta:
        model = Todos
        fields = ('id', 'task', 'urgent', 'important', 'category', 'user', 'tags')
        depth = 1