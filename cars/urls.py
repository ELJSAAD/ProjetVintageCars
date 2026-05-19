from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('connexion/',   views.connexion,    name='connexion'),
    path('deconnexion/', views.deconnexion,  name='deconnexion'),

    # Dashboard (redirige selon rôle)
    path('',                         views.dashboard,               name='dashboard'),
    path('conservateur/dashboard/',  views.dashboard_conservateur,  name='dashboard_conservateur'),
    path('mecanicien/dashboard/',    views.dashboard_mecanicien,    name='dashboard_mecanicien'),

    # Véhicules
    path('vehicules/',                          views.vehicules,            name='vehicules'),
    path('vehicules/nouveau/',                  views.enregistrer_vehicule, name='enregistrer_vehicule'),
    path('vehicules/<int:pk>/',                 views.detail_vehicule,      name='detail_vehicule'),
    path('vehicules/<int:pk>/modifier/',        views.modifier_vehicule,    name='modifier_vehicule'),
    path('vehicules/<int:pk>/supprimer/',       views.supprimer_vehicule,   name='supprimer_vehicule'),
    path('vehicules/<int:pk>/statut/',          views.modifier_statut,      name='modifier_statut'),

    # Interventions
    path('interventions/nouvelle/',             views.saisir_intervention,          name='saisir_intervention'),
    path('vehicules/<int:pk>/intervention/',    views.saisir_intervention,          name='saisir_intervention_vehicule'),

    # Taux restauration
    path('restauration/',  views.taux_restauration,  name='taux_restauration'),

    # Gérer utilisateurs (conservateur)
    path('utilisateurs/', views.gerer_utilisateurs, name='gerer_utilisateurs'),

]