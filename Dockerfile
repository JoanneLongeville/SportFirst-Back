# Utiliser l'image de base Python. Si manque de place, utiliser python:3.12-slim
FROM python:3.12.0

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le contenu actuel du répertoire local dans le répertoire de travail du conteneur
COPY . /app

# Installer les dépendances de l'application Python avec pip
RUN python -m pip install --upgrade pip --no-cache-dir -r requirements.txt

# Exposer le port utilisé par l'application 
EXPOSE 8080

# Commande par défaut à exécuter lorsque le conteneur démarre
CMD ["python", "main.py"]

