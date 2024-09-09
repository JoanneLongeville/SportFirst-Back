package domain

import "mymodule/internal/model"

// UserRepository définit l'interface pour les opérations de la base de données liées aux utilisateurs.
type UserRepository interface {
	CreateUser(user model.User) error
	EmailExists(email string) (bool, error)
	UpdatePassword(user *model.User, hashedPassword string) error
	GetUserByResetToken(token string) (*model.User, error)
	SaveResetToken(email string, token string) error
	SaveResetTokenAndNewPassword(email, token, newPassword string) error
	DeleteResetToken(email string) error
	GetUserByEmail(email string) (*model.User, error)
}
