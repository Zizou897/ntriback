from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewset import *

router = DefaultRouter()
# router.register(r'nutritionnistes', NutritionnisteViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'rendezvous', RendezVousViewSet)
router.register(r'conseils', ConseilViewSet)
router.register(r'messages', MessageViewSet)
# router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
