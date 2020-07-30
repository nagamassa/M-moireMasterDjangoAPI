from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions, viewsets

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from authapp.models import *
from authapp.serializers import *

# Create your views here.

# ======================================================================================================================
# ================================================ path des localites ==================================================
# ======================================================================================================================
@csrf_exempt
def localite_list(request):
    if request.method == 'GET':
        localites = Localite.objects.all()
        localites_serializer = LocaliteSerializer(localites, many=True)
        return JsonResponse(localites_serializer.data, safe=False)
    elif request.method == 'POST':
        localite_data = JSONParser().parse(request)
        localite_serializer = LocaliteSerializer(data=localite_data)
        if localite_serializer.is_valid():
            localite_serializer.save()
            return JsonResponse(localite_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(localite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def localite_users(request, pk):
    try:
        localite = Localite.objects.get(pk=pk)
        try:
            users = User.objects.filter(localite=localite)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Localite.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        users_serializer = UserCreateSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

@csrf_exempt
def localite_detail(request, pk):
    try:
        localite = Localite.objects.get(pk=pk)
    except Localite.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        localite_serializer = LocaliteSerializer(localite)
        return JsonResponse(localite_serializer.data)
    elif request.method == 'PUT':
        localite_data = JSONParser().parse(request)
        localite_serializer = LocaliteSerializer(localite, data=localite_data)
        if localite_serializer.is_valid():
            localite_serializer.save()
            return JsonResponse(localite_serializer.data)
        return JsonResponse(localite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def localite_list_region(request, region):
    localites = Localite.objects.filter(region=region)
    if request.method == 'GET':
        localites_serializer = LocaliteSerializer(localites, many=True)
        return JsonResponse(localites_serializer.data, safe=False)

# ======================================================================================================================
# ================================================ path des utilisateurs ===============================================
# ======================================================================================================================
@csrf_exempt
def change_password(request, pk, code):
    utilisateur = User.objects.get(pk=pk)
    utilisateur.is_active = True
    utilisateur.set_password(code)
    utilisateur.save()
    if request.method == 'PUT':
        if utilisateur:
            return JsonResponse(utilisateur.password,status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse('',status=status.HTTP_400_BAD_REQUEST, safe=False)

@csrf_exempt
def change_notification(request, pk, idnot):
    utilisateur = User.objects.get(pk=pk)
    utilisateur.is_active = True
    utilisateur.idNotification = idnot;
    utilisateur.save()
    if request.method == 'PUT':
        if utilisateur:
            return JsonResponse(utilisateur.idNotification, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse('echec', status=status.HTTP_400_BAD_REQUEST, safe=False)


@csrf_exempt
def findByPhone(request, phone):
    try:
        utilisateur = User.objects.filter(phone__contains=phone).get()
    except User.DoesNotExist:
        return HttpResponse('Faux', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        utilisateur_serializer = UserCreateSerializer(utilisateur)
        if utilisateur:
            return JsonResponse(utilisateur_serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(utilisateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def utilisateur_list(request):
    if request.method == 'GET':
        utilisateurs = User.objects.all()
        utilisateurs_serializer = UserCreateSerializer(utilisateurs, many=True)
        return JsonResponse(utilisateurs_serializer.data, safe=False)
    elif request.method == 'POST':
        utilisateur_data = JSONParser().parse(request)
        utilisateur_serializer = UserCreateSerializer(data=utilisateur_data)
        if utilisateur_serializer.is_valid():
            utilisateur_serializer.save()
            return JsonResponse(utilisateur_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(utilisateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def utilisateur_detail(request, pk):
    try:
        utilisateur = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        utilisateur_serializer = UserCreateSerializer(utilisateur)
        return JsonResponse(utilisateur_serializer.data)
    elif request.method == 'PUT':
        utilisateur_data = JSONParser().parse(request)
        utilisateur_serializer = UserCreateSerializer(utilisateur, data=utilisateur_data)
        if utilisateur_serializer.is_valid():
            utilisateur_serializer.save()
            return JsonResponse(utilisateur_serializer.data)
        return JsonResponse(utilisateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def mes_groupes(request, pk):
    try:
        owner = User.objects.get(pk=pk)
        try:
            groupes = Groupe.objects.filter(membre__user_member=owner , membre__isFondateur="Vrai")
        except Groupe.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        groupes_serializer = GroupeSerializer(groupes, many=True)
        return JsonResponse(groupes_serializer.data, safe=False)

@csrf_exempt
def mes_groupes_link(request, pk):
    try:
        owner = User.objects.get(pk=pk)
        try:
            groupes = Groupe.objects.filter(membre__user_member=owner , membre__isFondateur="Faux")
        except Groupe.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        groupes_serializer = GroupeSerializer(groupes, many=True)
        return JsonResponse(groupes_serializer.data, safe=False)

@csrf_exempt
def groupe_auteur(request, pk):
    try:
        groupe = Groupe.objects.get(pk=pk)
        try:
            user = User.objects.filter(membre__groupe=groupe , membre__isFondateur="Vrai").get()
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Groupe.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = UserCreateSerializer(user)
        return JsonResponse(user_serializer.data)

@csrf_exempt
def groupe_membre_user(request, pk):
    try:
        groupe = Groupe.objects.get(pk=pk)
        try:
            users = User.objects.filter(membre__groupe=groupe)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Groupe.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = UserCreateSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)




# ======================================================================================================================
# ================================================ path des alertes ====================================================
# ======================================================================================================================
@csrf_exempt
def alerte_list(request):
    if request.method == 'GET':
        alertes = Alerte.objects.all()
        alertes_serializer = AlerteSerializer(alertes, many=True)
        return JsonResponse(alertes_serializer.data, safe=False)
    elif request.method == 'POST':
        alerte_data = JSONParser().parse(request)
        alerte_serializer = AlerteSerializer(data=alerte_data)
        if alerte_serializer.is_valid():
            alerte_serializer.save()
            return JsonResponse(alerte_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(alerte_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_detail(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        alerte_serializer = AlerteSerializer(alerte)
        return JsonResponse(alerte_serializer.data)
    elif request.method == 'PUT':
        alerte_data = JSONParser().parse(request)
        alerte_serializer = AlerteSerializer(alerte, data=alerte_data)
        if alerte_serializer.is_valid():
            alerte_serializer.save()
            return JsonResponse(alerte_serializer.data)
        return JsonResponse(alerte_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        alerte.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class PieceView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    piece_serializer = PieceJointeSerializer(data=request.data)
    if piece_serializer.is_valid():
      piece_serializer.save()
      return Response(piece_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(piece_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_pieces(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            pieces = PieceJointe.objects.filter(alerte=alerte)
        except PieceJointe.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        pieces_serializer = PieceJointeSerializer(pieces, many=True)
        return JsonResponse(pieces_serializer.data, safe=False)
    elif request.method == 'POST':
        piece_data = JSONParser().parse(request)
        piece_serializer = PieceJointeSerializer(data=piece_data)
        if piece_serializer.is_valid():
            piece_serializer.save()
            return JsonResponse(piece_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(piece_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def alerte_pieces_details(request, pk, id):
    piece = PieceJointe.objects.get(pk=id)
    if request.method == 'GET':
        piece_serializer = PieceJointeSerializer(piece)
        return JsonResponse(piece_serializer.data)

@csrf_exempt
def alerte_suivi_perso(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            followers = SuiviAlertePerso.objects.filter(alerte=alerte)
        except SuiviAlertePerso.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        followers_serializer = SuiviAlertePersoSerializer(followers, many=True)
        return JsonResponse(followers_serializer.data, safe=False)
    elif request.method == 'POST':
        follower_data = JSONParser().parse(request)
        follower_serializer = SuiviAlertePersoSerializer(data=follower_data)
        if follower_serializer.is_valid():
            follower_serializer.save()
            return JsonResponse(follower_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(follower_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def alerte_suivi_perso_users(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            users = User.objects.filter(suivialerteperso__alerte=alerte)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = UserCreateSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)

@csrf_exempt
def alerte_suivi_perso_details(request, pk, id):
    try:
        follower = SuiviAlertePerso.objects.get(pk=id)
    except SuiviAlertePerso.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        follower_serializer = SuiviAlertePersoSerializer(follower)
        return JsonResponse(follower_serializer.data)
    elif request.method == 'PUT':
        follower_data = JSONParser().parse(request)
        follower_serializer = SuiviAlertePersoSerializer(follower, data=follower_data)
        if follower_serializer.is_valid():
            follower_serializer.save()
            return JsonResponse(follower_serializer.data)
        return JsonResponse(follower_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        follower.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


def alerte_suivi_perso_filtre(request, pk, id):
    try:
        alerte = Alerte.objects.get(pk=id)
        try:
            user = User.objects.get(pk=pk)
            try:
                follower = SuiviAlertePerso.objects.filter(alerte=alerte, follower=user).get()
            except SuiviAlertePerso.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        follower_serializer = SuiviAlertePersoSerializer(follower)
        return JsonResponse(follower_serializer.data)
    elif request.method == 'PUT':
        follower_data = JSONParser().parse(request)
        follower_serializer = SuiviAlertePersoSerializer(follower, data=follower_data)
        if follower_serializer.is_valid():
            follower_serializer.save()
            return JsonResponse(follower_serializer.data)
        return JsonResponse(follower_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def alerte_suivi_group(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            sGroupes = SuiviAlerteGroupe.objects.filter(alerte=alerte)
        except SuiviAlerteGroupe.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sGroupes_serializer = SuiviAlerteGroupeSerializer(sGroupes, many=True)
        return JsonResponse(sGroupes_serializer.data, safe=False)
    elif request.method == 'POST':
        sGroupe_data = JSONParser().parse(request)
        sGroupe_serializer = SuiviAlerteGroupeSerializer(data=sGroupe_data)
        if sGroupe_serializer.is_valid():
            sGroupe_serializer.save()
            return JsonResponse(sGroupe_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(sGroupe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_suivi_group_data(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            groupes = Groupe.objects.filter(suivialertegroupe__alerte=alerte)
        except SuiviAlerteGroupe.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        groupes_serializer = GroupeSerializer(groupes, many=True)
        return JsonResponse(groupes_serializer.data, safe=False)

@csrf_exempt
def alerte_suivi_group_details(request, pk, id):
    try:
        sGroupe = SuiviAlerteGroupe.objects.get(pk=id)
    except SuiviAlertePerso.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sGroupe_serializer = SuiviAlerteGroupeSerializer(sGroupe)
        return JsonResponse(sGroupe_serializer.data)
    elif request.method == 'DELETE':
        sGroupe.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def alerte_suivi_localite(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            sLocalites = SuiviAlerteLocalite.objects.filter(alerte=alerte)
        except SuiviAlerteLocalite.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sLocalites_serializer = SuiviAlerteLocaliteSerializer(sLocalites, many=True)
        return JsonResponse(sLocalites_serializer.data, safe=False)
    elif request.method == 'POST':
        sLocalite_data = JSONParser().parse(request)
        sLocalite_serializer = SuiviAlerteLocaliteSerializer(data=sLocalite_data)
        if sLocalite_serializer.is_valid():
            sLocalite_serializer.save()
            return JsonResponse(sLocalite_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(sLocalite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_suivi_localite_data(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            localites = Localite.objects.filter(suivialertelocalite__alerte=alerte)
        except Localite.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        localites_serializer = LocaliteSerializer(localites, many=True)
        return JsonResponse(localites_serializer.data, safe=False)

@csrf_exempt
def alerte_suivi_localite_users(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            localites = Localite.objects.filter(suivialertelocalite__alerte=alerte)
        except Localite.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        localites_serializer = LocaliteSerializer(localites, many=True)
        return JsonResponse(localites_serializer.data, safe=False)


@csrf_exempt
def alerte_suivi_localite_details(request, pk, id):
    try:
        sLocalite = SuiviAlerteLocalite.objects.get(pk=id)
    except SuiviAlerteLocalite.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sLocalite_serializer = SuiviAlerteLocaliteSerializer(sLocalite)
        return JsonResponse(sLocalite_serializer.data)
    elif request.method == 'DELETE':
        sLocalite.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def alerte_suivi_agence(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            sAgences = SuiviAlerteAgence.objects.filter(alerte=alerte)
        except SuiviAlerteAgence.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sAgences_serializer = SuiviAlerteGroupeSerializer(sAgences, many=True)
        return JsonResponse(sAgences_serializer.data, safe=False)
    elif request.method == 'POST':
        sAgence_data = JSONParser().parse(request)
        sAgence_serializer = SuiviAlerteLocaliteSerializer(data=sAgence_data)
        if sAgence_serializer.is_valid():
            sAgence_serializer.save()
            return JsonResponse(sAgence_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(sAgence_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_suivi_agence_details(request, pk, id):
    try:
        sAgence = SuiviAlerteAgence.objects.get(pk=id)
    except SuiviAlerteAgence.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sAgence_serializer = SuiviAlerteAgenceSerializer(sAgence)
        return JsonResponse(sAgence_serializer.data)

@csrf_exempt
def alerte_suivi_agence(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            sAgences = SuiviAlerteAgence.objects.filter(alerte=alerte)
        except SuiviAlerteAgence.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sAgences_serializer = SuiviAlerteGroupeSerializer(sAgences, many=True)
        return JsonResponse(sAgences_serializer.data, safe=False)
    elif request.method == 'POST':
        sAgence_data = JSONParser().parse(request)
        sAgence_serializer = SuiviAlerteLocaliteSerializer(data=sAgence_data)
        if sAgence_serializer.is_valid():
            sAgence_serializer.save()
            return JsonResponse(sAgence_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(sAgence_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_suivi_agence_details(request, pk, id):
    try:
        sAgence = SuiviAlerteAgence.objects.get(pk=id)
    except SuiviAlerteAgence.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        sAgence_serializer = SuiviAlerteAgenceSerializer(sAgence)
        return JsonResponse(sAgence_serializer.data)

def alerte_coordonnees(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
        try:
            coord = Coordonnees.objects.filter(alerte=alerte)
        except Coordonnees.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        coordonnees_serializer = CoordonneesSerializer(coord, many=True)
        return JsonResponse(coordonnees_serializer.data, safe=False)
    elif request.method == 'POST':
        coordonnees_data = JSONParser().parse(request)
        coordonnees_serializer = CoordonneesSerializer(data=coordonnees_data)
        if coordonnees_serializer.is_valid():
            coordonnees_serializer.save()
            return JsonResponse(coordonnees_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(coordonnees_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def alerte_coordonnees_details(request, pk, id):
    try:
        coordonnees = Coordonnees.objects.get(pk=id)
    except Coordonnees.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        coordonnees_serializer = CoordonneesSerializer(coordonnees)
        return JsonResponse(coordonnees_serializer.data)

@csrf_exempt
def mes_alertes(request, id):
    try:
        auteur = User.objects.get(pk=id)
        try:
            alertes = Alerte.objects.filter(auteur=auteur)
        except Alerte.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        alertes_serializer = AlerteSerializer(alertes, many=True)
        return JsonResponse(alertes_serializer.data, safe=False)

@csrf_exempt
def mes_alertes_prog(request, id):
    try:
        auteur = User.objects.get(pk=id)
        try:
            alertes = Alerte.objects.filter(auteur=auteur, statut='Inactive', type = 'Programmée', utilisee = 'Faux')
        except Alerte.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        alertes_serializer = AlerteSerializer(alertes, many=True)
        return JsonResponse(alertes_serializer.data, safe=False)

@csrf_exempt
def autres_alertes(request, id):
    try:
        auteur = User.objects.get(pk=id)
        try:
            alertes = Alerte.objects.filter(suivialerteperso__follower=auteur).exclude(auteur=auteur)
        except Alerte.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        alertes_serializer = AlerteSerializer(alertes, many=True)
        return JsonResponse(alertes_serializer.data, safe=False)

@csrf_exempt
def alerte_auteur(request, pk):
    try:
        alerte = Alerte.objects.get(pk=pk)
    except Alerte.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        auteur = alerte.auteur
        auteur_serializer = UserCreateSerializer(auteur)
        return JsonResponse(auteur_serializer.data)


# ======================================================================================================================
# ================================================ path des Groupes ====================================================
# ======================================================================================================================
@csrf_exempt
def groupe_list(request):
    if request.method == 'GET':
        groupes = Groupe.objects.all()
        groupes_serializer = GroupeSerializer(groupes, many=True)
        return JsonResponse(groupes_serializer.data, safe=False)
    elif request.method == 'POST':
        groupe_data = JSONParser().parse(request)
        groupe_serializer = GroupeSerializer(data=groupe_data)
        if groupe_serializer.is_valid():
            groupe_serializer.save()
            return JsonResponse(groupe_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(groupe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def groupe_detail(request, pk):
    try:
        groupe = Groupe.objects.get(pk=pk)
    except Groupe.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        groupe_serializer = GroupeSerializer(groupe)
        return JsonResponse(groupe_serializer.data)
    elif request.method == 'PUT':
        groupe_data = JSONParser().parse(request)
        groupe_serializer = GroupeSerializer(groupe, data=groupe_data)
        if groupe_serializer.is_valid():
            groupe_serializer.save()
            return JsonResponse(groupe_serializer.data)
        return JsonResponse(groupe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        groupe.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# ======================================================================================================================
# ================================================ path des Membres de Groupes ====================================================
# ======================================================================================================================
@csrf_exempt
def groupe_membre(request, pk):
    try:
        groupe = Groupe.objects.get(pk=pk)
    except Groupe.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        membres = Membre.objects.filter(groupe=groupe)
        membres_serializer = MembreSerializer(membres, many=True)
        return JsonResponse(membres_serializer.data, safe=False)
    elif request.method == 'POST':
        membre_data = JSONParser().parse(request)
        membre_serializer = MembreSerializer(data=membre_data)
        if membre_serializer.is_valid():
            membre_serializer.save()
            return JsonResponse(membre_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(membre_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def groupe_membre_detail(request, pk, id):
    try:
        membre = Membre.objects.get(pk=id)
    except Membre.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        membre_serializer = MembreSerializer(membre)
        return JsonResponse(membre_serializer.data)
    elif request.method == 'PUT':
        membre_data = JSONParser().parse(request)
        membre_serializer = MembreSerializer(membre, data=membre_data)
        if membre_serializer.is_valid():
            membre_serializer.save()
            return JsonResponse(membre_serializer.data)
        return JsonResponse(membre_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        membre.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def groupe_user_membre_detail(request, pk, id):
    membre = Membre.objects.get(pk=id)
    user = User.objects.get(pk=membre.user_member.id)
    if request.method == 'GET':
        user_serializer = UserCreateSerializer(user)
        return JsonResponse(user_serializer.data)

@csrf_exempt
def groupe_user_membre_localite(request, pk, id):
    membre = Membre.objects.get(pk=id)
    user = User.objects.get(pk=membre.user_member.id)
    localite = Localite.objects.get(pk=user.localite.id)
    if request.method == 'GET':
        localite_serializer = LocaliteSerializer(localite)
        return JsonResponse(localite_serializer.data)

