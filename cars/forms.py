from dataclasses import fields

from django import forms
from .models import Marque, Vehicule, Intervention, STATUT_CHOICES


# Formulaire de connexion (même style que club_sportif)
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')


# Formulaire pour enregistrer / modifier un véhicule (conservateur)
class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['marque', 'modele', 'annee', 'chassis', 'statut', 'cylindres', 'cylindree']

    def clean_annee(self):
        annee = self.cleaned_data.get('annee')
        if annee and (annee < 1900 or annee > 1999):
            raise forms.ValidationError("Seuls les véhicules vintage (1900–1999) sont acceptés.")
        return annee

    def clean_chassis(self):
        chassis = self.cleaned_data.get('chassis')
        if chassis and len(chassis) != 17:
            raise forms.ValidationError("Le numéro VIN doit contenir exactement 17 caractères.")
        return chassis.upper()


# Formulaire pour modifier uniquement le statut
class StatutForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['statut']


# Formulaire pour saisir une intervention
class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['vehicule', 'type', 'date', 'cout']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# Formulaire de recherche / filtrage véhicules
class RechercheForm(forms.Form):
    q = forms.CharField(required=False, label='Recherche libre')
    marque = forms.ModelChoiceField(
        queryset=Marque.objects.all(),
        required=False, empty_label='Toutes les marques'
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + STATUT_CHOICES,
        required=False
    )
    annee_min = forms.IntegerField(required=False, label='Année min')
    annee_max = forms.IntegerField(required=False, label='Année max')


















