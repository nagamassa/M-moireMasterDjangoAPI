
"""
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Localite(models.Model):
    region = models.CharField(max_length=20)
    adresse = models.CharField(max_length=50)
    def __str__(self):
        return self.region+' => '+self.adresse


class Utilisateur(models.Model):
    choixProfil = [('Simple','Simple'),('Admin','Admin'),('Policier','Policier'),('Gendarme','Gendarme'),('Pompier','Pompier')]
    choixStatut = [('Anonyme', 'Anonyme'), ('Public', 'Public'),]
    choixBlocage = [('Vrai', 'Vrai'), ('Faux', 'Faux'), ]
    blocage = models.CharField(max_length=10, choices=choixBlocage, default=choixBlocage[1])
    profil = models.CharField(max_length=10, choices=choixProfil, default=choixProfil[0])
    statut = models.CharField(max_length=10, choices=choixStatut, default=choixStatut[1])
    alias = models.CharField(max_length=20)
    phone = models.IntegerField(unique=True)
    dateNaissance = models.DateField()
    description = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    bloques = models.ManyToManyField('self', through='Bloccage', symmetrical=False)

    def __str__(self):
        return self.alias+' => '+self.user.first_name+' => '+self.profil

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(args, **kwargs)



class Bloccage(models.Model):
    choixbloc = [('Bloqué', 'Bloqué'), ('Débloqué', 'Débloqué')]
    bloqueur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='bloqueur')
    bloque = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='bloque')
    raison = models.TextField()
    statut = models.CharField(max_length=10, choices=choixbloc, default=choixbloc[0])

    class Meta:
        db_table = 'Bloccage'
        constraints = [
            models.UniqueConstraint(fields=['bloqueur', 'bloque'], name='unique_blocage')
        ]

    def __str__(self):
        return 'bloqueur='+self.bloqueur.alias+" => bloque="+self.bloque.alias+" => "+self.raison



class Groupe(models.Model):
    nombreMembre = models.IntegerField(default=0)
    nom = models.CharField(max_length=50)
    dateCreation = models.DateTimeField(auto_now_add=True)
    membres = models.ManyToManyField(Utilisateur, through='Membre')

    def __str__(self):
        return self.nom

class Membre(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    choixProfil = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    choixFondateur = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    isAdmin = models.CharField(max_length=5, choices=choixProfil, default=choixProfil[1])
    isFondateur = models.CharField(max_length=5, choices=choixFondateur, default=choixFondateur[1])
    dateJoined = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Membre'
        constraints = [
            models.UniqueConstraint(fields=['groupe', 'utilisateur'], name='unique_membre')
        ]

    def __str__(self):
        return self.utilisateur.alias+" => "+self.groupe.nom+" => "+self.get_isFondateur_display()


class Alerte(models.Model):
    choixStatut = [('Active', 'Active'), ('Inactive', 'Inactive')]
    choixProfil = [('Anonyme', 'Anonyme'), ('Public', 'Public')]
    profil = models.CharField(max_length=10, choices=choixProfil, default=choixProfil[0])
    statut = models.CharField(max_length=10, choices=choixStatut, default=choixStatut[0])
    dateAlerte = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    groupes = models.ManyToManyField(Groupe, through='SuiviAlerteGroupe')
    localites = models.ManyToManyField(Localite, through='SuiviAlerteLocalite')

    def __str__(self):
        return str(self.id)+" => "+self.get_statut_display()+" => "+self.utilisateur.alias


class SuiviAlerteLocalite(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    nombreReception = models.IntegerField(default=0)
    nombreReponse = models.IntegerField(default=0)

    class Meta:
        db_table = 'SuiviAlerteLocalite'
        constraints = [
            models.UniqueConstraint(fields=['localite', 'alerte'], name='unique_suivi_localite')
        ]

    def __str__(self):
        return self.localite.adresse+' => '+str(self.nombreReception)+' => '+str(self.nombreReponse)+' => '+self.alerte.utilisateur.alias


class SuiviAlerteGroupe(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    nombreReception = models.IntegerField(default=0)
    nombreReponse = models.IntegerField(default=0)

    class Meta:
        db_table = 'SuiviAlerteGroupe'
        constraints = [
            models.UniqueConstraint(fields=['groupe', 'alerte'], name='unique_suivi_groupe')
        ]

    def __str__(self):
        return self.groupe.nom+' => '+str(self.nombreReception)+' => '+str(self.nombreReponse)+' => '+self.alerte.utilisateur.alias


class SuiviAlertePerso(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    choixReception = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    choixReponse = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    reception = models.CharField(max_length=5, choices=choixReception, default=choixReception[1])
    reponse = models.CharField(max_length=5, choices=choixReponse, default=choixReponse[1])
    DateReception = models.DateTimeField(blank=True, null=True)
    DateReponse = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'SuiviAlerte'
        constraints = [
            models.UniqueConstraint(fields=['alerte', 'utilisateur'], name='unique_suivi_perso')
        ]

    def __str__(self):
        return self.utilisateur.alias+' => '+self.reception+' => '+self.reponse+' => '+self.alerte.utilisateur.alias


class TextAlerte(models.Model):
    texte = models.TextField()
    dateTexte = models.DateTimeField(auto_now_add=True)
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)

    def __str__(self):
        return self.texte+' => '+self.alerte.utilisateur.alias+' => '+str(self.dateTexte)

class TextAlerteSugession(models.Model):
    titre = models.CharField(max_length=20)
    texte = models.TextField()
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre+' => '+self.utilisateur.alias+' => '+self.texte

class Coordonnees(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE,blank=True, null=True)
    dateCoordonnees = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)
    latitude = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return str(self.longitude)+' => '+str(self.latitude)+' => '+str(self.dateCoordonnees)


class Article(models.Model):
    choixbloc = [('Bloqué', 'Bloqué'), ('Débloqué', 'Débloqué')]
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    choixType = [('Recherché', 'Recherché'),('Fugitif', 'Fugitif'),('Possession illégale d"arme', 'Possession illégale d"arme'),('Fraude', 'Fraude'),('Corruption', 'Corruption'),('Meurtre', 'Meurtre'), ('Cambriolage', 'Cambriolage'), ('Escroquerie', 'Escroquerie'), ('Agression', 'Agression'), ('Braquage', 'Braquage'), ('Trafic de drogue', 'Trafic de drogue'), ('Disparition', 'Disparition'), ('Vol', 'Vol'), ('Enlèvement', 'Enlèvement'), ('Viol', 'Viol'), ('Autre', 'Autre')]
    choixSituation = [('Résolue', 'Résolue'), ('Non résolu', 'Non résolu')]
    choixStatut = [('Anonyme', 'Anonyme'), ('Public', 'Public')]
    choixlienPosteur = [('Victime', 'Victime'), ('Témoin', 'Témoin'), ('Voisin', 'Voisin'), ('Policier', 'Policier'), ('Gendarme', 'Gendarme'), ('Sapeur-pompier', 'Sapeur-pompier'), ('Autre', 'Autre')]
    type = models.CharField(max_length=30, choices=choixType)
    situation = models.CharField(max_length=15, choices=choixSituation, default=choixSituation[1])
    statut = models.CharField(max_length=10, choices=choixStatut, default=choixStatut[0])
    lienPosteur = models.CharField(max_length=20, choices=choixlienPosteur)
    titre = models.CharField(max_length=100)
    details = models.TextField()
    blocage = models.CharField(max_length=20, choices=choixbloc, default=choixbloc[1])
    dateArticle = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type+' => '+self.utilisateur.alias+' => '+self.titre


class Personne(models.Model):
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    choixProfil = [('Coupable', 'Coupable'),('Suspect', 'Suspect'),('Enlevé', 'Enlevé'),('Disparu', 'Disparu'),('Fugitif', 'Fugitif'),('Victime', 'Victime'),('Recherché', 'Recherché'), ('A se méfier', 'A se méfier'), ('Autre', 'Autre')]
    choixGenre = [('Inconnu', 'Inconnu'),('Femme', 'Femme'),('Homme', 'Homme')]
    profil = models.CharField(max_length=30, choices=choixProfil)
    nom = models.CharField(max_length=30, blank=True, null=True)
    prenom = models.CharField(max_length=30, blank=True, null=True)
    alias = models.CharField(max_length=30)
    genre = models.CharField(max_length=30, choices=choixGenre)
    age = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.profil+' => '+self.alias+' => '+self.article.titre

class PieceJointe(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE, blank=True, null=True)
    choixType = [('Audio','Audio'),('Vidéo','Vidéo'),('Photo','Photo')]
    choixProprio = [('Article','Article'),('Alerte','Alerte')]
    proprio = models.CharField(max_length=10, choices=choixProprio)
    type = models.CharField(max_length=10, choices=choixType)
    titre = models.CharField(max_length=50, blank=True, null=True)
    piece = models.FileField(upload_to='pieces_jointes/')

    def __str__(self):
        return self.type+' => '+self.proprio

    def delete(self, *args, **kwargs):
        self.piece.delete()
        super().delete(args, **kwargs)


class Signal(models.Model):
    choixObjet = [('Propos mensongers', 'Propos mensongers'),('Non respect des regles', 'Non respect des regles'), ('Propos choquants ou déplacés', 'Propos choquants ou déplacés'), ('Audio, vidéo ou photo choquant', 'Audio, vidéo ou photo choquant'), ('Autre', 'Autre')]
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    objet = models.CharField(max_length=50, choices=choixObjet)
    details = models.TextField()

    def __str__(self):
        return self.utilisateur.alias+' => '+self.objet+' => '+self.article.titre

    class Meta:
        db_table = 'Signal'
        constraints = [
            models.UniqueConstraint(fields=['article', 'utilisateur'], name='unique_signal')
        ]


class Agence(models.Model):
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    coordonnees = models.OneToOneField(Coordonnees, on_delete=models.CASCADE)
    choixType = [('Police','Police'),('Gendarmerie','Gendarmerie'),('Sapeur-pompier','Sapeur-pompier'),('Autre','Autre')]
    type = models.CharField(max_length=20, choices=choixType)
    nom = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100, blank=True, null=True)
    alertes = models.ManyToManyField(Alerte, through='SuiviAlerteAgence')
    def __str__(self):
        return self.nom+' => '+self.localite.region+' => '+self.localite.adresse


class AgenceLink(models.Model):
    choixAdmin = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    isAdmin = models.CharField(max_length=5, choices=choixAdmin, default=choixAdmin[1])
    dateAgenceLink = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.utilisateur.alias+' => '+self.agence.nom+' => '+str(self.dateAgenceLink)+' => '+self.isAdmin

    class Meta:
        db_table = 'AgenceLink'
        constraints = [
            models.UniqueConstraint(fields=['agence', 'utilisateur'], name='unique_agent_agence')
        ]

class SuiviAlerteAgence(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    nombreReception = models.IntegerField(default=0)
    nombreReponse = models.IntegerField(default=0)
    dateTransfert = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SuiviAlerteAgence'
        constraints = [
            models.UniqueConstraint(fields=['agence', 'alerte'], name='unique_suivi_agence')
        ]

    def __str__(self):
        return self.agence.nom + ' => ' +str(self.nombreReception) + ' => ' + str(self.nombreReponse) + ' => ' + self.alerte.utilisateur.alias
"""