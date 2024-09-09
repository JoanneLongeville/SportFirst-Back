package domain

import (
	"github.com/DATA-DOG/go-sqlmock"
	"mymodule/internal/model"
	"testing"
)

func TestCreateUser(t *testing.T) {

	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO users").
		WithArgs("Veronique", "Bernard", "Femme", "2000-01-01", "10 avenue Carnot 91300 Massy", "1234567890", "veronique.bernard@gmail.com", "password").
		WillReturnResult(sqlmock.NewResult(1, 1))

	repo := UserRepositoryImpl{DB: db}
	user := model.User{
		Firstname:   "Veronique",
		Lastname:    "Bernard",
		Gender:      "Femme",
		DateOfBirth: "2000-01-01",
		Address:     "10 avenue Carnot 91300 Massy",
		Phone:       "1234567890",
		Email:       "veronique.bernard@gmail.com",
		Password:    "password",
	}

	if err := repo.CreateUser(user); err != nil {
		t.Errorf("CreateUser failed: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %v", err)
	}
}

func TestEmailExists(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	rows := sqlmock.NewRows([]string{"count"}).AddRow(1)
	mock.ExpectQuery("SELECT COUNT\\(\\*\\) FROM users WHERE email = \\$1").
		WithArgs("veronique.bernard@gmail.com").
		WillReturnRows(rows)
	repo := UserRepositoryImpl{DB: db}

	email := "veronique.bernard@gmail.com"

	// Testing if EmailExists behaves as expected
	exists, err := repo.EmailExists(email)
	if err != nil {
		t.Errorf("EmailExists failed: %v", err)
	}
	if !exists {
		t.Errorf("EmailExists should return true for existing email")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %v", err)
	}

}

func TestUpdatePassword(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}
	defer db.Close()

	repo := &UserRepositoryImpl{DB: db}

	email := "user@example.com"
	newPassword := "newPassword123"
	query := "UPDATE users SET password = $2 WHERE email = $1"
	mock.ExpectExec(query).
		WithArgs(email, newPassword).
		WillReturnResult(sqlmock.NewResult(1, 1))

	user := &model.User{
		Email: email,
	}

	err = repo.UpdatePassword(user, newPassword)
	if err != nil {
		t.Errorf("UpdatePassword failed: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("there were unfulfilled expectations: %v", err)
	}
}
