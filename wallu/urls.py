from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
# ==================== path des localites ========================
    path('wallu/localites/', views.localite_list, name='list_localite'),

    path('wallu/localites/<pk>/users/', views.localite_users, name='users_localite'),

    path('wallu/localites/<pk>/', views.localite_detail, name='detail_localite'),
    path('wallu/localites/region/<region>/', views.localite_list_region, name='filtre_localite'),

# ==================== path des utilisateurs ========================
    path('wallu/utilisateurs/', views.utilisateur_list, name='list_utilisateur'),
    path('wallu/utilisateurs/findByPhone/<phone>/', views.findByPhone, name='find_by_phone'),
    path('wallu/utilisateurs/<pk>/myGroupes/', views.mes_groupes, name='mes_groupes'),
    path('wallu/utilisateurs/<pk>/myGroupesLinked/', views.mes_groupes_link, name='mes_groupes_link'),
    path('wallu/utilisateurs/<pk>/', views.utilisateur_detail, name='detail_utilisateur'),
    path('wallu/utilisateurs/<pk>/change_notification/<idnot>/', views.change_notification, name='change_notification'),
    path('wallu/utilisateurs/<pk>/<code>/', views.change_password, name='change_password'),


# ==================== path des alertes ========================
    path('wallu/alertes/', views.alerte_list, name='list_alerte'),
    path('wallu/alertes/mines/<id>/', views.mes_alertes, name='mes_alertes'),
    path('wallu/alertes/others/<id>/', views.autres_alertes, name='autres_alertes'),
    path('wallu/alertes/<pk>/', views.alerte_detail, name='detail_alerte'),
    path('wallu/alertes/<pk>/auteur/', views.alerte_auteur, name='auteur_alerte'),
    path('wallu/alertes/<pk>/coordonnees/', views.alerte_coordonnees, name='alerte_coordonnees'),
    path('wallu/alertes/<pk>/coordonnees/<id>/', views.alerte_coordonnees_details, name='alerte_coordonnees_details'),
    path('wallu/alertes/<pk>/pieces/', views.alerte_pieces, name='alerte_pieces'),
    path('wallu/alertes/<pk>/piecesUpload/', views.PieceView.as_view(), name='alerte_pieces'),

    path('wallu/alertes/suivi_perso/<pk>/<id>/', views.alerte_suivi_perso_filtre, name='alerte_suivi_perso_filtre'),

    path('wallu/alertes/<pk>/pieces/<id>/', views.alerte_pieces_details, name='alerte_pieces_details'),
    path('wallu/alertes/<pk>/suivi_perso/', views.alerte_suivi_perso, name='alerte_suivi_perso'),
    path('wallu/alertes/<pk>/suivi_perso/users/', views.alerte_suivi_perso_users, name='alerte_suivi_perso_users'),
    path('wallu/alertes/<pk>/suivi_perso/<id>/', views.alerte_suivi_perso_details, name='alerte_suivi_perso_details'),
    path('wallu/alertes/<pk>/suivi_groups/', views.alerte_suivi_group, name='alerte_suivi_group'),
    path('wallu/alertes/<pk>/suivi_groups/data/', views.alerte_suivi_group_data, name='alerte_suivi_group_data'),
    path('wallu/alertes/<pk>/suivi_groups/<id>/', views.alerte_suivi_group_details, name='alerte_suivi_group_details'),
    path('wallu/alertes/<pk>/suivi_localites/', views.alerte_suivi_localite, name='alerte_suivi_localite'),
    path('wallu/alertes/<pk>/suivi_localites/data/', views.alerte_suivi_localite_data, name='alerte_suivi_localite_data'),
    path('wallu/alertes/<pk>/suivi_localites/<id>/', views.alerte_suivi_localite_details, name='alerte_suivi_localite_details'),
    path('wallu/alertes/<pk>/suivi_agences/', views.alerte_suivi_agence, name='alerte_suivi_agence'),
    path('wallu/alertes/<pk>/suivi_agences/<id>/', views.alerte_suivi_agence_details, name='alerte_suivi_agence_details'),

# ==================== path des groupes ========================
    path('wallu/groupes/', views.groupe_list, name='list_groupe'),
    path('wallu/groupes/<pk>/auteur/', views.groupe_auteur, name='groupe_auteur'),
    path('wallu/groupes/<pk>/membres/users/', views.groupe_membre_user, name='groupe_membre_user'),
    path('wallu/groupes/<pk>/', views.groupe_detail, name='detail_groupe'),
    path('wallu/groupes/<pk>/membres/', views.groupe_membre, name='membres_groupe'),
    path('wallu/groupes/<pk>/membres/<id>/', views.groupe_membre_detail, name='membre_groupe_detail'),
    path('wallu/groupes/<pk>/membres/<id>/user/', views.groupe_user_membre_detail, name='user_membre_groupe_detail'),
    path('wallu/groupes/<pk>/membres/<id>/user/localite/', views.groupe_user_membre_localite, name='user_membre_groupe_localite'),


]


if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

