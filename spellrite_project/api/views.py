from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Teacher, SpellingList, SpellingListWord
from .serializers import TeacherSerializer, SpellingListSerializer, SpellingListWordSerializer, TeacherDetailSerializer, RegistrationSerializer 
from .permissions import IsAdminOrSelf, IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Teachers.
    Includes an action to retrieve detailed teacher information.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer

    def get_permissions(self):
        # For actions that require object-level permissions
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(TeacherViewSet, self).get_permissions()


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Endpoint to retrieve the authenticated teacher's information.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# class SpellingListViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing Spelling Lists.
#     """
#     queryset = SpellingList.objects.all()
#     serializer_class = SpellingListSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class SpellingListWordViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing Words within a Spelling List.
#     """
#     queryset = SpellingListWord.objects.all()
#     serializer_class = SpellingListWordSerializer
#     permission_classes = [permissions.IsAuthenticated]

class SpellingListWordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing words within spelling lists.
    Only allows access to words belonging to the authenticated teacher's lists.
    """
    serializer_class = SpellingListWordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter words to only those in spelling lists owned by the authenticated teacher
        return SpellingListWord.objects.filter(spelling_list__teacher=self.request.user)

    def perform_create(self, serializer):
        # Check that the spelling list provided belongs to the authenticated teacher
        spelling_list = serializer.validated_data.get('spelling_list')
        if spelling_list.teacher != self.request.user:
            raise PermissionDenied("You do not own this spelling list.")
        serializer.save()

class SpellingListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Spelling Lists.
    """
    serializer_class = SpellingListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only return spelling lists for the authenticated teacher
        return SpellingList.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        # Associate the new spelling list with the authenticated teacher
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwner])
    def add_word(self, request, pk=None):
        """
        Custom action to add a word to a specific spelling list.
        """
        spelling_list = self.get_object()  # Ensures list belongs to the teacher
        word_text = request.data.get('word')
        if not word_text:
            return Response({'error': 'Word not provided'}, status=400)
        
        # Create a new SpellingListWord for the list
        new_word = SpellingListWord.objects.create(spelling_list=spelling_list, word=word_text)
        serializer = SpellingListWordSerializer(new_word)
        return Response(serializer.data, status=201)

class RegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny] 