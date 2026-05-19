# 🚗 VintageCars

Application Django de gestion d'une collection de voitures vintages.

## Structure du projet

```
ProjetVintageCars/
├── cars/               ← Application principale Django
├── VintageCars/        ← Configuration du projet
├── templates/          ← Templates HTML globaux
├── vintagecars.db      ← Base de données SQLite
├── manage.py
└── README.md
```

## Rôles utilisateurs

- **Conservateur** : gestion complète (véhicules, utilisateurs, statistiques)
- **Mécanicien** : consultation et saisie d'interventions

## Lancer le projet

```bash
pip install django
python manage.py migrate
python manage.py runserver
```
