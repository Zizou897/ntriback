from django.db import models
from django.contrib.auth import get_user_model
from core.constants import ARTICLE_IMG_PATH



User = get_user_model()


class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notif pour {self.utilisateur.email}"


class Nutritionniste(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Actif', 'Actif'), ('Inactif', 'Inactif')], default='Actif')

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('InActive', 'InActive')], default='Active')

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    image = models.ImageField(upload_to=ARTICLE_IMG_PATH, blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    nutritionniste = models.ForeignKey(Nutritionniste, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Publié', 'Publié'), ('Brouillon', 'Brouillon'), ('Supprimé', 'Supprimé')], default='Publié')

    def __str__(self):
        return self.titre


class Patient(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Actif', 'Actif'), ('Inactif', 'Inactif')], default='Actif')

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class RendezVous(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(max_length=15, choices=[('Confirmé', 'Confirmé'), ('Annulé', 'Annulé'), ('En attente', 'En attente')], default='En attente')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nutritionniste = models.ForeignKey(Nutritionniste, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Actif', 'Actif'), ('Annulé', 'Annulé'), ('Terminé', 'Terminé')], default='Actif')

    def __str__(self):
        return f"Rendez-vous {self.date} - {self.heure}"


class Conseil(models.Model):
    contenu = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nutritionniste = models.ForeignKey(Nutritionniste, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Actif', 'Actif'), ('Archivé', 'Archivé')], default='Actif')

    def __str__(self):
        return f"Conseil pour {self.patient}"


class Message(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('Nouveau', 'Nouveau'), ('Lu', 'Lu'), ('Archivé', 'Archivé')], default='Nouveau')

    def __str__(self):
        return f"Message de {self.nom}"


class Journal(models.Model):
    ACTIONS = [
        ("login", "Connexion"),
        ("create_rdv", "Création Rendez-vous"),
        ("update_profile", "Mise à jour profil"),
        ("password_reset", "Réinitialisation mot de passe"),
        # ajoute ce que tu veux
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTIONS)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} @ {self.created_at}"
    


class Contact(models.Model):
    nom = models.CharField(max_length=255)
    sujet = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Contact de {self.nom}"