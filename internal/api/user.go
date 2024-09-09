package api

import (
	"github.com/gin-gonic/gin"
	"log"
	"mymodule/internal/domain"
	"mymodule/internal/model"
	"mymodule/pkg"
	"net/http"
)

// CreateUserHandler est un Handler pour créer les utilisateurs.
func CreateUserHandler(userRepo domain.UserRepository) gin.HandlerFunc {
	return func(c *gin.Context) {
		var newUser model.User

		// Lier l'entrée JSON à la structure newUser
		if err := c.ShouldBindJSON(&newUser); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request data"})
			return
		}

		// Vérifier si l'adresse e-mail existe déjà
		exists, err := userRepo.EmailExists(newUser.Email)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error checking if email exists"})
			return
		}

		if exists {
			c.JSON(http.StatusConflict, gin.H{"error": "Vous avez déjà un compte"})
			return
		}

		// Vérifier l'e-mail avec l'API Hunter
		hunterResponse, err := domain.VerifyEmailWithHunter(newUser.Email)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error verifying email with Hunter"})
			return
		}

		if hunterResponse.Data.Status != "valid" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid email address"})
			return
		}

		// Utilisez HashPassword de pkg utils.go
		hashedPassword, err := pkg.HashPassword(newUser.Password)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error hashing password"})
			return
		}
		newUser.Password = hashedPassword

		// Utiliser UUID de pkg utils.go
		uuid, err := pkg.GenerateUUID()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error generating verification UUID"})
			return
		}

		// Définir l'UUID comme token de l'utilisateur
		newUser.Token = uuid

		// Créer l'utilisateur
		if err := userRepo.CreateUser(newUser); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error creating user"})
			return
		}

		c.JSON(http.StatusCreated, gin.H{"message": "User created successfully"})
	}
}

func RequestResetPasswordHandler(userRepo domain.UserRepository, emailSender *pkg.EmailSender) gin.HandlerFunc {
	return func(c *gin.Context) {
		var request struct {
			Email string `json:"email"`
		}

		// Lier l'entrée JSON à la structure request
		if err := c.ShouldBindJSON(&request); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request data"})
			return
		}

		// Vérifier si l'adresse e-mail existe
		exists, err := userRepo.EmailExists(request.Email)
		if err != nil {
			log.Printf("Error checking if email exists: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error checking if email exists"})
			return
		}

		if !exists {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Email not found"})
			return
		}

		// Générer le token de réinitialisation
		resetToken, err := pkg.GenerateUUID()
		if err != nil {
			log.Printf("Error generating reset token: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to generate reset token"})
			return
		}

		// Sauvegarder le token de réinitialisation dans la base de données
		if err := userRepo.SaveResetToken(request.Email, resetToken); err != nil {
			log.Printf("Error saving reset token: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save reset token"})
			return
		}

		// Construire le lien de réinitialisation
		resetLink := "http://localhost:8084/reset-password?token=" + resetToken

		// Envoyer l'e-mail avec le lien de réinitialisation
		if err := emailSender.SendResetEmail(request.Email, resetLink); err != nil {
			log.Printf("Error sending reset email: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to send reset email"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"message": "Reset email sent successfully"})
	}
}

func ResetPasswordHandler(userRepo domain.UserRepository) gin.HandlerFunc {
	return func(c *gin.Context) {
		var request struct {
			Token       string `json:"token"`
			NewPassword string `json:"newPassword"`
		}

		if err := c.ShouldBindJSON(&request); err != nil {
			log.Printf("Error binding JSON: %v", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request data"})
			return
		}

		user, err := userRepo.GetUserByResetToken(request.Token)
		if err != nil {
			log.Printf("Error getting user by reset token: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error checking reset token"})
			return
		}
		if user == nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid or expired reset token"})
			return
		}

		hashedPassword, err := pkg.HashPassword(request.NewPassword)
		if err != nil {
			log.Printf("Error hashing password: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error hashing new password"})
			return
		}

		if err := userRepo.UpdatePassword(user, hashedPassword); err != nil {
			log.Printf("Error updating password: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update password"})
			return
		}

		if err := userRepo.DeleteResetToken(user.Email); err != nil {
			log.Printf("Error deleting reset token: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete reset token"})
			return
		}

		log.Printf("Password reset successfully for user: %v", user.Email)
		c.JSON(http.StatusOK, gin.H{"message": "Password has been reset successfully"})
	}
}

func LoginHandler(userRepo domain.UserRepository) gin.HandlerFunc {
	return func(c *gin.Context) {
		var loginDetails struct {
			Email    string `json:"email"`
			Password string `json:"password"`
		}

		// Log de début de traitement
		log.Println("LoginHandler started")

		// Lier l'entrée JSON à la structure loginDetails
		if err := c.ShouldBindJSON(&loginDetails); err != nil {
			log.Printf("Error binding JSON: %v", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request data"})
			return
		}

		// Log de détail de connexion
		log.Printf("Attempting login for email: %s", loginDetails.Email)

		user, err := userRepo.GetUserByEmail(loginDetails.Email)
		if err != nil {
			log.Printf("Error retrieving user: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error retrieving user"})
			return
		}

		if user == nil {
			log.Println("User not found or invalid credentials")
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
			return
		}

		// Vérifier le mot de passe
		if !pkg.ComparePasswords(user.Password, loginDetails.Password) {
			log.Println("Invalid password")
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid email or password"})
			return
		}

		// Authentification réussie, renvoyer les informations de l'utilisateur
		c.JSON(http.StatusOK, gin.H{
			"message":       "Successfully logged in",
			"userID":        user.ID,
			"userFirstname": user.Firstname,
		})
	}
}

// UserRoutes définit les routes utilisateur.
func UserRoutes(router *gin.Engine, userRepo domain.UserRepository, emailSender *pkg.EmailSender) {
	// Création de compte
	router.POST("/create-account", CreateUserHandler(userRepo))

	// Demande de réinitialisation du mot de passe
	router.POST("/request-reset-password", RequestResetPasswordHandler(userRepo, emailSender))

	// Réinitialisation du mot de passe
	router.POST("/reset-password", ResetPasswordHandler(userRepo))

	// Connexion de l'utilisateur
	router.POST("/login", LoginHandler(userRepo))
}
