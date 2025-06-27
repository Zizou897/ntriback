from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now
from .models import Nutritionniste, Categorie, Article, Patient, RendezVous, Conseil, Message, Notification, Journal, Contact





@admin.register(Nutritionniste)
class NutritionnisteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'status', 'date_ajout')
    search_fields = ('nom', 'email')
    list_filter = ('status',)



@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('action', 'ip_address', 'description', 'created_at')
    search_fields = ('action',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'lu', 'date_envoi')
    list_filter = ('lu',)




@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'status', 'date_ajout')
    search_fields = ('nom',)
    list_filter = ('status',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nutritionniste', 'categorie', 'status', 'date_publication')
    search_fields = ('titre', 'contenu')
    list_filter = ('status', 'categorie')
    autocomplete_fields = ('categorie', 'nutritionniste')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'status')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('status',)

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('date', 'heure', 'patient', 'nutritionniste', 'statut')
    list_filter = ('statut',)
    search_fields = ('patient__nom', 'nutritionniste__nom')

@admin.register(Conseil)
class ConseilAdmin(admin.ModelAdmin):
    list_display = ('patient', 'nutritionniste', 'date_ajout', 'status')
    list_filter = ('status',)
    search_fields = ('patient__nom', 'nutritionniste__nom')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'status', 'date_envoi')
    list_filter = ('status',)
    search_fields = ('nom', 'email')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_envoi')
    search_fields = ('nom', 'email')
