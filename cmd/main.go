package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"log"
	"mymodule/internal/api"
	"mymodule/internal/domain"
	"mymodule/pkg"
	"os"
)

func main() {
	// Charger les variables d'environnement depuis le fichier .env
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	// Récupérer les configurations SMTP depuis les variables d'environnement
	smtpHost := os.Getenv("SMTPHost")
	smtpPort := os.Getenv("SMTPPort")
	smtpEmail := os.Getenv("SMTPEmail")

	// Vérifier que toutes les variables d'environnement SMTP nécessaires sont définies
	if smtpHost == "" || smtpPort == "" || smtpEmail == "" {
		log.Fatal("SMTP configuration is missing in .env file")
	}

	// Initialiser EmailSender avec les paramètres SMTP
	emailSender := pkg.NewEmailSender(smtpHost, smtpPort, smtpEmail)

	// Initialiser la connexion à la base de données
	db, err := pkg.NewDB("config/config.yaml")
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer db.Close()

	// Initialiser le repository utilisateur
	userRepo := &domain.UserRepositoryImpl{DB: db}

	// Configurer et démarrer le serveur Gin
	router := gin.Default()
	configureCORS(router)

	// Définir les routes pour l'API
	api.UserRoutes(router, userRepo, emailSender)

	// Démarrer le serveur sur le port 8080
	log.Fatal(router.Run(":8080"))
}

func configureCORS(router *gin.Engine) {
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"*"}
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type"}
	router.Use(cors.New(config))
}
