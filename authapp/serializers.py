from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, generics
from .models import *

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','last_login','is_superuser','username','password','first_name','last_name','is_staff','is_active','date_joined','email','blocage','profil','statut','alias','idNotification','phone','dateNaissance','description','photo','localite')

# ====================================================

class LocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localite
        fields = ('id','region','adresse')

# ====================================================

class BloccageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloccage
        fields = ('id','bloqueur','bloque','raison','statut')

# ====================================================

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = ('id','nombreMembre','nom','dateCreation')

# ====================================================

class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = ('id','user_member','groupe','isAdmin','isFondateur','dateJoined')

# ====================================================

class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ('id','profil','statut','dateAlerte','auteur', 'titre', 'utilisee','type')

# ====================================================

class SuiviAlerteLocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviAlerteLocalite
        fields = ('id','alerte','localite','nombreReception','nombreReponse')

# ====================================================

class SuiviAlerteGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviAlerteGroupe
        fields = ('id','alerte','groupe','nombreReception','nombreReponse')

# ====================================================

class SuiviAlertePersoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviAlertePerso
        fields = ('id','alerte','follower','reception','reponse','DateReception','DateReponse')

# ====================================================

class CoordonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordonnees
        fields = ('id','alerte','dateCoordonnees','longitude','latitude')

# ====================================================

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','localite','auteur','type','situation','statut','lienPosteur','titre','details','blocage','dateArticle')

# ====================================================

class PersonneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personne
        fields = ('id','localite','article','profil','nom','prenom','alias','genre','age','description')

# ====================================================

class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = ('id','article','alerte','proprio','type','titre','piece','texto','datePiece')

# ====================================================

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ('id','article','utilisateur','objet','details')

# ====================================================

class AgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agence
        fields = ('id','localite','coordonnees','type','nom','phone','email')

# ====================================================

class AgenceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenceLink
        fields = ('id','agence','agent','isAdmin','dateAgenceLink')

# ====================================================

class SuiviAlerteAgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviAlerteAgence
        fields = ('id','alerte','agence','nombreReception','nombreReponse','dateTransfert')