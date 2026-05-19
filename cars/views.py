from urllib import request

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count

from .models import Marque, Vehicule, Intervention, Profil
from .forms import ConnexionForm, VehiculeForm, StatutForm, InterventionForm, RechercheForm



# CONNEXION / DECONNEXION  — UseCase : s'authentifier

def connexion(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('connexion')



# DASHBOARD — redirige selon le rôle (conservateur / mécanicien)

@login_required(login_url='connexion')
def dashboard(request):
    role = request.user.profil.role
    if role == 'conservateur':
        return redirect('dashboard_conservateur')
    else:
        return redirect('dashboard_mecanicien')



# DASHBOARD CONSERVATEUR (admin)

@login_required(login_url='connexion')
def dashboard_conservateur(request):
    if request.user.profil.role != 'conservateur':
        return redirect('dashboard_mecanicien')

    nb_vehicules    = Vehicule.objects.count()
    nb_interventions = Intervention.objects.count()
    total_cout      = Intervention.objects.aggregate(t=Sum('cout'))['t'] or 0
    nb_restaures    = Vehicule.objects.filter(statut='restaure').count()
    nb_en_restauration = Vehicule.objects.filter(statut='en_restauration').count()
    nb_en_attente   = Vehicule.objects.filter(statut='en_attente').count()

    context = {
        'nb_vehicules': nb_vehicules,
        'nb_interventions': nb_interventions,
        'total_cout': total_cout,
        'nb_restaures': nb_restaures,
        'nb_en_restauration': nb_en_restauration,
        'nb_en_attente': nb_en_attente,
    }
    return render(request, 'dashboard_conservateur.html', context)



# DASHBOARD MÉCANICIEN

@login_required(login_url='connexion')
def dashboard_mecanicien(request):
    if request.user.profil.role != 'mecanicien':
        return redirect('dashboard_conservateur')

    # Le mécanicien voit les dernières interventions et peut chercher des véhicules
    dernieres_interventions = Intervention.objects.select_related('vehicule').order_by('-date')[:5]
    context = {'dernieres_interventions': dernieres_interventions}
    return render(request, 'dashboard_mecanicien.html', context)



# VÉHICULES — UseCase : rechercher/filtrer

@login_required(login_url='connexion')
def vehicules(request):
    form = RechercheForm(request.GET or None)
    liste = Vehicule.objects.select_related('marque').all()

    if form.is_valid():
        q        = form.cleaned_data.get('q')
        marque   = form.cleaned_data.get('marque')
        statut   = form.cleaned_data.get('statut')
        annee_min = form.cleaned_data.get('annee_min')
        annee_max = form.cleaned_data.get('annee_max')
        if q:
            liste = liste.filter(
                Q(modele__icontains=q) |
                Q(marque__nom_marque__icontains=q) |
                Q(chassis__icontains=q)
            )
        if marque:
            liste = liste.filter(marque=marque)
        if statut:
            liste = liste.filter(statut=statut)
        if annee_min:
            liste = liste.filter(annee__gte=annee_min)
        if annee_max:
            liste = liste.filter(annee__lte=annee_max)
    return render(request, 'vehicules.html', {'vehicules': liste, 'form': form})



# ENREGISTRER UN VÉHICULE — UseCase : enregistrer un vehicule

@login_required(login_url='connexion')
def enregistrer_vehicule(request):
    if request.user.profil.role != 'conservateur':
        messages.error(request, "Accès réservé au conservateur.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            v = form.save()
            messages.success(request, f"Véhicule « {v} » enregistré avec succès.")
            return redirect('vehicules')
    else:
        form = VehiculeForm()
    return render(request, 'vehicule_form.html', {'form': form, 'titre': 'Enregistrer un véhicule', 'action': 'Enregistrer'})



# MODIFIER LA FICHE TECHNIQUE — UseCase : modifier la fiche technique

@login_required(login_url='connexion')
def modifier_vehicule(request, pk):
    if request.user.profil.role != 'conservateur':
        messages.error(request, "Accès réservé au conservateur.")
        return redirect('dashboard')

    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            messages.success(request, "Fiche technique mise à jour.")
            return redirect('detail_vehicule', pk=pk)
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'vehicule_form.html', {'form': form, 'vehicule': vehicule, 'titre': f'Modifier — {vehicule}', 'action': 'Enregistrer'})



# SUPPRIMER UN VÉHICULE (conservateur)

@login_required(login_url='connexion')
def supprimer_vehicule(request, pk):
    if request.user.profil.role != 'conservateur':
        return redirect('dashboard')
    vehicule = get_object_or_404(Vehicule, pk=pk)
    vehicule.delete()
    messages.success(request, "Véhicule supprimé.")
    return redirect('vehicules')



# DÉTAIL VÉHICULE

@login_required(login_url='connexion')
def detail_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule.objects.select_related('marque'), pk=pk)
    interventions = vehicule.interventions.order_by('-date')
    cout_total = interventions.aggregate(t=Sum('cout'))['t'] or 0
    return render(request, 'detail_vehicule.html', {
        'vehicule': vehicule,
        'interventions': interventions,
        'cout_total': cout_total,
    })



# MODIFIER LE STATUT — UseCase : modifier le statut du vehicule

@login_required(login_url='connexion')
def modifier_statut(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = StatutForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            messages.success(request, f"Statut mis à jour : {vehicule.get_statut_display()}")
            return redirect('detail_vehicule', pk=pk)
    else:
        form = StatutForm(instance=vehicule)
    return render(request, 'modifier_statut.html', {'form': form, 'vehicule': vehicule})



# SAISIR UNE INTERVENTION — UseCase : saisir une intervention

@login_required(login_url='connexion')
def saisir_intervention(request, pk=None):
    vehicule = get_object_or_404(Vehicule, pk=pk) if pk else None
    initial = {'vehicule': vehicule} if vehicule else {}

    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            i = form.save()
            messages.success(request, "Intervention enregistrée.")
            return redirect('detail_vehicule', pk=i.vehicule.pk)
    else:
        form = InterventionForm(initial=initial)
    return render(request, 'intervention_form.html', {'form': form, 'vehicule': vehicule})



# TAUX DE RESTAURATION — UseCase : consulter taux restauration

@login_required(login_url='connexion')
def taux_restauration(request):
    total = Vehicule.objects.count()
    restaures = Vehicule.objects.filter(statut='restaure').count()
    taux = round(restaures / total * 100, 1) if total > 0 else 0
    cout_global = Intervention.objects.aggregate(t=Sum('cout'))['t'] or 0

    vehicules = Vehicule.objects.select_related('marque').annotate(
        nb_interventions=Count('interventions'),
        cout_total=Sum('interventions__cout')
    ).order_by('-cout_total')

    par_marque = Marque.objects.annotate(
        nb=Count('vehicules'),
        cout=Sum('vehicules__interventions__cout')
    ).filter(nb__gt=0).order_by('-cout')

    return render(request, 'taux_restauration.html', {
        'total': total,
        'restaures': restaures,
        'taux': taux,
        'cout_global': cout_global,
        'vehicules': vehicules,
        'par_marque': par_marque,
    })



# GÉRER LES UTILISATEURS — UseCase : gérer les utilisateurs (conservateur)

@login_required(login_url='connexion')
def gerer_utilisateurs(request):
    if request.user.profil.role != 'conservateur':
        messages.error(request, "Accès réservé au conservateur.")
        return redirect('dashboard')

    from django.contrib.auth.models import User
    if request.method == 'POST':
        # Modifier le rôle d'un utilisateur
        user_id = request.POST.get('user_id')
        nouveau_role = request.POST.get('role')
        profil = get_object_or_404(Profil, utilisateur_id=user_id)
        profil.role = nouveau_role
        profil.save()
        messages.success(request, "Rôle mis à jour.")
        return redirect('gerer_utilisateurs')

    utilisateurs = Profil.objects.select_related('utilisateur').all()
    return render(request, 'utilisateurs.html', {'utilisateurs': utilisateurs})


