from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from .serializer import *

# class NutritionnisteViewSet(viewsets.ModelViewSet):
#     queryset = Nutritionniste.objects.all()
#     serializer_class = NutritionnisteSerializer
#     permission_classes = [IsAuthenticated]

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(status="Publié").order_by("-date_ajout")
    serializer_class = ArticleSerializer
    
    @action(detail=False, methods=["get"], url_path="recents")
    def get_recent_articles(self, request):
        latest_articles = self.queryset[:3]
        serializer = self.get_serializer(latest_articles, many=True)
        return Response(serializer.data)
    

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]
    

class ConseilViewSet(viewsets.ModelViewSet):
    queryset = Conseil.objects.all()
    serializer_class = ConseilSerializer
    permission_classes = [IsAuthenticated]
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class ContactViewSet(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Envoi des emails ici (comme vu précédemment)...
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)