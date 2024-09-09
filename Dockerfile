# Utilisation de l'image de base Go
FROM golang:latest

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers go.mod et go.sum (si existants) et télécharger les dépendances
COPY go.mod go.sum ./
RUN go mod download

# Copier le reste des fichiers du projet
COPY . .

# Compiler l'application
RUN go build -o main ./cmd/...

# Exposer le port utilisé par l'application (si nécessaire)
EXPOSE 8080

# Lancer l'application en utilisant le fichier de configuration YAML
CMD ["./main", "-config=config.yaml"]

