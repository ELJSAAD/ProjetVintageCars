from django.db import models
from django.contrib.auth.models import User  # on utilise le User Django natif comme club_sportif


#--DEBUT CLASS PROFIL--
class Profil(models.Model):
    ROLES = [('conservateur', 'Conservateur'), ('mecanicien', 'Mécanicien')]
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='mecanicien')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.role}"
#--FIN CLASS PROFIL--


#--DEBUT CLASS MARQUE--
class Marque(models.Model):
    # Champs du diagramme de classes
    nom_marque = models.CharField(max_length=100)       # nom_marque:Charfield
    pays_origine = models.CharField(max_length=100)     # pays_origine:Charfield

    def __str__(self):                                  # +__str__():str
        return self.nom_marque
#--FIN CLASS MARQUE--


#--DEBUT CLASS VEHICULE--
STATUT_CHOICES = [
    ('en_restauration', 'En restauration'),
    ('restaure', 'Restauré'),
    ('en_attente', 'En attente'),
    ('a_vendre', 'À vendre'),
]

class Vehicule(models.Model):
    # Champs du diagramme de classes
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='vehicules')  # marque:FK(Marque)
    modele = models.CharField(max_length=150)           # modele:Charfield
    annee = models.IntegerField()                       # annee:Integerfield
    chassis = models.CharField(max_length=17, unique=True)  # chassis:Charfield(VIN)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')  # statut:Charfield
    cylindres = models.IntegerField()                   # cylindres:Integerfield
    cylindree = models.IntegerField()                   # cylindree:Integerfield

    def get_decade(self):                               # +get_decade();str
        """Retourne la décennie du véhicule. Ex: 1965 → '1960s'"""
        return f"{(self.annee // 10) * 10}s"

    def __str__(self):
        return f"{self.marque.nom_marque} {self.modele} ({self.annee})"
#--FIN CLASS VEHICULE--


#--DEBUT CLASS INTERVENTION--
class Intervention(models.Model):
    # Champs du diagramme de classes
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='interventions')  # vehicule:FK(vehicule)
    type = models.CharField(max_length=200)           
    date = models.DateField()                           
    cout = models.DecimalField(max_digits=10, decimal_places=2)  # cout:Decimalfield

    def __str__(self):                                  # +__str__():str
        return f"{self.type} - {self.vehicule} ({self.date})"
#--FIN CLASS INTERVENTION--
