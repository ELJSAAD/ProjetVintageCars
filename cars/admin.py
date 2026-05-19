from django.contrib import admin
from .models import Profil, Marque, Vehicule, Intervention

# Register your models here.
admin.site.register(Profil)
admin.site.register(Marque)
admin.site.register(Vehicule)
admin.site.register(Intervention)