from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Localite(models.Model):
    region = models.CharField(max_length=20)
    adresse = models.CharField(max_length=50)
    def __str__(self):
        return self.region+' => '+self.adresse

class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    choixProfil = [('Simple', 'Simple'), ('Admin', 'Admin'), ('Policier', 'Policier'), ('Gendarme', 'Gendarme'),
                   ('Pompier', 'Pompier')]
    choixStatut = [('Anonyme', 'Anonyme'), ('Public', 'Public'), ]
    choixBlocage = [('Vrai', 'Vrai'), ('Faux', 'Faux'), ]
    blocage = models.CharField(max_length=10, choices=choixBlocage, default='Faux')
    profil = models.CharField(max_length=10, choices=choixProfil, default='Simple')
    statut = models.CharField(max_length=10, choices=choixStatut, default='Public')
    alias = models.CharField(max_length=20, null=True, blank=True)
    idNotification = models.CharField(max_length=200, default='nothing')
    phone = models.IntegerField(unique=True, null=True, blank=True)
    dateNaissance = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE, null=True, blank=True)
    bloques = models.ManyToManyField('self', through='Bloccage', symmetrical=False)
#    REQUIRED_FIELDS=['username','phone','first_name','last_name']
#    USERNAME_FIELD = 'email'

#    def get_username(self):
#        return self.email



    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(args, **kwargs)


class Bloccage(models.Model):
    choixbloc = [('Bloqué', 'Bloqué'), ('Débloqué', 'Débloqué')]
    bloqueur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bloqueur')
    bloque = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bloque')
    raison = models.TextField()
    statut = models.CharField(max_length=10, choices=choixbloc, default='Bloqué')

    class Meta:
        db_table = 'Bloccage'
        constraints = [
            models.UniqueConstraint(fields=['bloqueur', 'bloque'], name='unique_blocage')
        ]

    def __str__(self):
        return 'bloqueur='+self.bloqueur.alias+" => bloque="+self.bloque.alias+" => "+self.raison


class Groupe(models.Model):
    nombreMembre = models.IntegerField(default=1)
    nom = models.CharField(max_length=50)
    dateCreation = models.DateTimeField(auto_now_add=True)
    membres = models.ManyToManyField(User, through='Membre')

    def __str__(self):
        return self.nom

class Membre(models.Model):
    user_member = models.ForeignKey(User, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    choixProfil = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    choixFondateur = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    isAdmin = models.CharField(max_length=5, choices=choixProfil, default='Faux')
    isFondateur = models.CharField(max_length=5, choices=choixFondateur, default='Faux')
    dateJoined = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Membre'
        constraints = [
            models.UniqueConstraint(fields=['groupe', 'user_member'], name='unique_user_member')
        ]

    def __str__(self):
        return self.user_member.alias+" => "+self.groupe.nom+" => "+self.get_isFondateur_display()


class Alerte(models.Model):
    choixUtilisee = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    choixType = [('Directe', 'Directe'), ('Programmée', 'Programmée')]
    choixStatut = [('Active', 'Active'), ('Inactive', 'Inactive')]
    choixProfil = [('Anonyme', 'Anonyme'), ('Public', 'Public')]
    titre = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=10, choices=choixType, default='Directe')
    profil = models.CharField(max_length=10, choices=choixProfil, default='Anonyme')
    statut = models.CharField(max_length=10, choices=choixStatut, default='Active')
    dateAlerte = models.DateTimeField(auto_now_add=True)
    utilisee = models.CharField(max_length=10, choices=choixUtilisee, default='Vrai')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    groupes = models.ManyToManyField(Groupe, through='SuiviAlerteGroupe')
    localites = models.ManyToManyField(Localite, through='SuiviAlerteLocalite')

    def __str__(self):
        return str(self.id)+" => "+self.get_statut_display()+" => "+self.auteur.alias


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
        return self.localite.adresse+' => '+str(self.nombreReception)+' => '+str(self.nombreReponse)+' => '+self.alerte.auteur.alias


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
        return self.groupe.nom+' => '+str(self.nombreReception)+' => '+str(self.nombreReponse)+' => '+self.alerte.auteur.alias


class SuiviAlertePerso(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    choixReception = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    choixReponse = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    reception = models.CharField(max_length=5, choices=choixReception, default='Faux')
    reponse = models.CharField(max_length=5, choices=choixReponse, default='Faux')
    DateReception = models.DateTimeField(blank=True, null=True)
    DateReponse = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'SuiviAlertePerso'
        constraints = [
            models.UniqueConstraint(fields=['alerte', 'follower'], name='unique_suivi_perso')
        ]

    def __str__(self):
        return self.follower.alias+' => '+self.reception+' => '+self.reponse+' => '+self.alerte.auteur.alias


#class TextAlerte(models.Model):
#    texte = models.TextField()
#    dateTexte = models.DateTimeField(auto_now_add=True)
#    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.texte+' => '+self.alerte.auteur.alias+' => '+str(self.dateTexte)

#class TextAlerteSugession(models.Model):
#    titre = models.CharField(max_length=20)
#    texte = models.TextField()
#    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.titre+' => '+self.auteur.alias+' => '+self.texte

class Coordonnees(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE,blank=True, null=True)
    dateCoordonnees = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=40, decimal_places=20)
    latitude = models.DecimalField(max_digits=40, decimal_places=20)

    def __str__(self):
        return str(self.longitude)+' => '+str(self.latitude)+' => '+str(self.dateCoordonnees)


class Article(models.Model):
    choixEtat = [('Préparation', 'Préparation'), ('Rejeté', 'Rejeté'), ('Accepté', 'Accepté'),  ('En cours de traitement', 'En cours de traitement')]
    localite = models.ForeignKey(Localite, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    choixType = [('Recherché', 'Recherché'),('Fugitif', 'Fugitif'),('Possession illégale d"arme', 'Possession illégale d"arme'),('Fraude', 'Fraude'),('Corruption', 'Corruption'),('Meurtre', 'Meurtre'), ('Cambriolage', 'Cambriolage'), ('Escroquerie', 'Escroquerie'), ('Agression', 'Agression'), ('Braquage', 'Braquage'), ('Trafic de drogue', 'Trafic de drogue'), ('Disparition', 'Disparition'), ('Vol', 'Vol'), ('Enlèvement', 'Enlèvement'), ('Viol', 'Viol'), ('Autre', 'Autre')]
    choixSituation = [('Résolue', 'Résolue'), ('Non résolu', 'Non résolu')]
    choixStatut = [('Anonyme', 'Anonyme'), ('Public', 'Public')]
    choixlienPosteur = [('Victime', 'Victime'), ('Témoin', 'Témoin'), ('Voisin', 'Voisin'), ('Policier', 'Policier'), ('Gendarme', 'Gendarme'), ('Sapeur-pompier', 'Sapeur-pompier'), ('Autre', 'Autre')]
    type = models.CharField(max_length=30, choices=choixType)
    situation = models.CharField(max_length=15, choices=choixSituation, default='Non résolu')
    statut = models.CharField(max_length=10, choices=choixStatut, default='Anonyme')
    lienPosteur = models.CharField(max_length=20, choices=choixlienPosteur)
    titre = models.CharField(max_length=100)
    details = models.TextField()
    etat = models.CharField(max_length=30, choices=choixEtat, default='Préparation')
    dateArticle = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type+' => '+self.auteur.alias+' => '+self.titre


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
    choixType = [('Audio','Audio'),('Vidéo','Vidéo'),('Photo','Photo'),('Texte','Texte')]
    choixProprio = [('Article','Article'),('Alerte','Alerte')]
    proprio = models.CharField(max_length=10, choices=choixProprio)
    type = models.CharField(max_length=10, choices=choixType)
    titre = models.CharField(max_length=50, blank=True, null=True)
    piece = models.FileField(upload_to='pieces_jointes/', null=True, blank=True)
    texto = models.TextField(null=True, blank=True)
    datePiece = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type+' => '+self.proprio

    def delete(self, *args, **kwargs):
        self.piece.delete()
        super().delete(args, **kwargs)


class Signal(models.Model):
    choixObjet = [('Propos mensongers', 'Propos mensongers'),('Non respect des regles', 'Non respect des regles'), ('Propos choquants ou déplacés', 'Propos choquants ou déplacés'), ('Audio, vidéo ou photo choquant', 'Audio, vidéo ou photo choquant'), ('Autre', 'Autre')]
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.CharField(max_length=50, choices=choixObjet)
    details = models.TextField()

    def __str__(self):
        return self.auteur.alias+' => '+self.objet+' => '+self.article.titre

    class Meta:
        db_table = 'Signal'
        constraints = [
            models.UniqueConstraint(fields=['article', 'auteur'], name='unique_signal')
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
    bloques = models.ManyToManyField(Article, through='Rejet')

    def __str__(self):
        return self.nom+' => '+self.localite.region+' => '+self.localite.adresse


class AgenceLink(models.Model):
    choixAdmin = [('Vrai', 'Vrai'), ('Faux', 'Faux')]
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)
    agent = models.OneToOneField(User, on_delete=models.CASCADE)
    isAdmin = models.CharField(max_length=5, choices=choixAdmin, default='Faux')
    dateAgenceLink = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent.alias+' => '+self.agence.nom+' => '+str(self.dateAgenceLink)+' => '+self.isAdmin

    class Meta:
        db_table = 'AgenceLink'
        constraints = [
            models.UniqueConstraint(fields=['agence', 'agent'], name='unique_agent_agence')
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
        return self.agence.nom + ' => ' +str(self.nombreReception) + ' => ' + str(self.nombreReponse) + ' => ' + self.alerte.auteur.alias

class Rejet(models.Model):
    bloqueur = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='bloqueur')
    bloque = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bloque')
    raison = models.TextField()
    dateRejet = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Rejet'
        constraints = [
            models.UniqueConstraint(fields=['bloqueur', 'bloque'], name='unique_rejet')
        ]

    def __str__(self):
        return 'bloqueur='+self.bloqueur.nom+" => bloque="+self.bloque.titre+" => "+self.raison