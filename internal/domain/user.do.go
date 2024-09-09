package domain

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"mymodule/internal/model"
	"net/http"
	"os"
)

const (
	hunterAPIEndpoint = "https://api.hunter.io/v2/email-verifier"
)

type UserRepositoryImpl struct {
	DB *sql.DB
}

type HunterVerifyResponse struct {
	Data struct {
		Status string `json:"status"`
	} `json:"data"`
}

// CreateUser insère un nouvel utilisateur dans la base de données.
func (repo *UserRepositoryImpl) CreateUser(user model.User) error {
	// Notez que la requête ne contient plus le champ date_of_birth ni les autres champs qui ne sont pas présents dans votre formulaire.
	query := `INSERT INTO users (firstname, lastname, phone, email, password, token) 
              VALUES ($1, $2, $3, $4, $5, $6)`
	_, err := repo.DB.Exec(query, user.Firstname, user.Lastname, user.Phone, user.Email, user.Password, user.Token)
	if err != nil {
		return fmt.Errorf("error creating user: %v", err)
	}
	return nil
}

// EmailExists vérifie si un e-mail existe déjà dans la base de données.
func (repo *UserRepositoryImpl) EmailExists(email string) (bool, error) {
	var count int
	query := "SELECT COUNT(*) FROM users WHERE email = $1"
	err := repo.DB.QueryRow(query, email).Scan(&count)
	if err != nil {
		log.Printf("Error executing query: %v\n", err)
		return false, fmt.Errorf("error checking if email exists: %v", err)
	}
	return count > 0, nil
}

// VerifyEmailWithHunter vérifie une adresse e-mail à l'aide de l'API Hunter
func VerifyEmailWithHunter(email string) (*HunterVerifyResponse, error) {
	hunterAPIKey := os.Getenv("HUNTER_API_KEY")
	if hunterAPIKey == "" {
		return nil, fmt.Errorf("Hunter API key is missing")
	}

	url := fmt.Sprintf("%s?email=%s&api_key=%s", hunterAPIEndpoint, email, hunterAPIKey)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result HunterVerifyResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return &result, nil
}

// UpdatePassword met à jour le mot de passe de l'utilisateur.
func (repo *UserRepositoryImpl) UpdatePassword(user *model.User, hashedPassword string) error {
	// La requête pour mettre à jour le mot de passe de l'utilisateur.
	query := "UPDATE users SET password = $2 WHERE email = $1"

	// Exécuter la requête avec le nouvel hashedPassword et l'email de l'utilisateur.
	result, err := repo.DB.Exec(query, user.Email, hashedPassword)
	if err != nil {
		log.Printf("Error updating password in database: %v", err)
		return fmt.Errorf("error updating password: %v", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		log.Printf("Error getting rows affected: %v", err)
	} else {
		log.Printf("Password updated for email %s, rows affected: %d", user.Email, rowsAffected)
	}

	return nil
}

// SaveResetToken enregistre un token de réinitialisation pour un utilisateur spécifique.
func (repo *UserRepositoryImpl) SaveResetToken(email string, token string) error {
	query := "UPDATE users SET reset_token = $2 WHERE email = $1"
	_, err := repo.DB.Exec(query, email, token)
	if err != nil {
		return fmt.Errorf("error saving reset token: %v", err)
	}
	return nil
}

// GetUserByResetToken récupère un utilisateur par son token de réinitialisation.
func (repo *UserRepositoryImpl) GetUserByResetToken(token string) (*model.User, error) {
	query := "SELECT id, firstname, lastname, gender, date_of_birth, address, zipcode, city, email, password, phone, token FROM users WHERE reset_token = $1"

	var user model.User
	err := repo.DB.QueryRow(query, token).Scan(&user.ID, &user.Firstname, &user.Lastname, &user.Gender, &user.DateOfBirth, &user.Address, &user.Zipcode, &user.City, &user.Email, &user.Password, &user.Phone, &user.Token)

	if errors.Is(err, sql.ErrNoRows) {
		log.Printf("No user found with reset token: %s", token)
		return nil, nil // Aucun utilisateur trouvé avec ce token
	} else if err != nil {
		log.Printf("Error retrieving user by reset token: %s, error: %v", token, err)
		return nil, err
	}

	log.Printf("User retrieved for reset token: %s, email: %s", token, user.Email)
	return &user, nil
}

// SaveResetTokenAndNewPassword sauvegarde un token de réinitialisation et un nouveau mot de passe hashé pour un utilisateur donné.
func (repo *UserRepositoryImpl) SaveResetTokenAndNewPassword(email, token, newPassword string) error {
	query := `UPDATE users SET token = $2, password = $3 WHERE email = $1`
	_, err := repo.DB.Exec(query, email, token, newPassword)
	if err != nil {
		// Gérer l'erreur
		return err
	}
	return nil
}

func (repo *UserRepositoryImpl) DeleteResetToken(email string) error {
	query := "UPDATE users SET reset_token = NULL WHERE email = $1"
	_, err := repo.DB.Exec(query, email)
	if err != nil {
		return fmt.Errorf("error deleting reset token: %v", err)
	}
	return nil
}

// GetUserByEmail récupère un utilisateur par son adresse e-mail.
func (repo *UserRepositoryImpl) GetUserByEmail(email string) (*model.User, error) {
	var user model.User

	query := "SELECT id, firstname, lastname, gender, date_of_birth, address, zipcode, city, email, password, phone, token, reset_token, role FROM users WHERE email = $1"

	// Log avant d'exécuter la requête
	log.Printf("Executing query: %s with email: %s", query, email)

	err := repo.DB.QueryRow(query, email).Scan(&user.ID, &user.Firstname, &user.Lastname, &user.Gender, &user.DateOfBirth, &user.Address, &user.Zipcode, &user.City, &user.Email, &user.Password, &user.Phone, &user.Token, &user.ResetToken, &user.Role)

	if err != nil {
		if err == sql.ErrNoRows {
			// Aucun utilisateur trouvé
			log.Printf("No user found with email: %s", email)
			return nil, nil
		}
		// Autre erreur de base de données
		log.Printf("Error retrieving user with email: %s, error: %v", email, err)
		return nil, err
	}

	// Log après avoir récupéré l'utilisateur avec succès
	log.Printf("User retrieved: %+v", user)

	return &user, nil
}
