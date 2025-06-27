import logging
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .models import *
from .serializer import *
from utils.loggers import log_action

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

from core import settings



User = get_user_model()
logger = logging.getLogger('app')


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        print("#################################")
        print(email)
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://127.0.0.1:8000/api/v1/password-reset-confirm/{uid}/{token}/"
            
            send_mail(
                subject="Réinitialisation de mot de passe",
                message=f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            return Response({"message": "Email de réinitialisation envoyé."})
        
        except User.DoesNotExist:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=404)
            


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
     
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                print(request.body)
                password = request.data.get("password")
                print("##############################")
                print(password)
                if password:
                    user.password = make_password(password)
                    user.save()
                    return Response({"message": "Mot de passe modifié avec succès."})
                return Response({"error": "Mot de passe requis."}, status=400)
            return Response({"error": "Token invalide."}, status=400)
        except Exception:
            return Response({"error": "Lien invalide."}, status=400)



class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(utilisateur=self.request.user).order_by('-date_envoi')


class MarquerCommeLueAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notif_id):
        try:
            notif = Notification.objects.get(pk=notif_id, utilisateur=request.user)
            notif.lu = True
            notif.save()
            logger.info(f"Notification marquée comme lue par {request.user}")
            return Response({"message": "Notification marquée comme lue."})
        except Notification.DoesNotExist:
            return Response({"error": "Notification non trouvée."}, status=404)
        


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            log_action(request, "login", "Connexion réussie.")
            logger.info(f"L'utilisateur {request.user} s'est connecté.")
        return response