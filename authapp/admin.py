from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Localite)
admin.site.register(User)
admin.site.register(Groupe)
admin.site.register(Membre)
admin.site.register(Alerte)
admin.site.register(SuiviAlerteGroupe)
admin.site.register(SuiviAlertePerso)
admin.site.register(SuiviAlerteLocalite)
admin.site.register(Article)
admin.site.register(Personne)
admin.site.register(Coordonnees)
admin.site.register(PieceJointe)
admin.site.register(Signal)
admin.site.register(Agence)
admin.site.register(AgenceLink)
admin.site.register(SuiviAlerteAgence)
admin.site.register(Bloccage)