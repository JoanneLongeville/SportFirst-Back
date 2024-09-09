package model

import "database/sql"

type User struct {
	ID          int            `json:"id"`
	Firstname   string         `json:"firstname"`
	Lastname    string         `json:"lastname"`
	Gender      sql.NullString `json:"gender"`
	DateOfBirth sql.NullString `json:"date_of_birth"`
	Address     sql.NullString `json:"address"`
	Zipcode     sql.NullString `json:"zipcode"`
	City        sql.NullString `json:"city"`
	Email       string         `json:"email"`
	Password    string         `json:"password"`
	Phone       string         `json:"phone"`
	Token       string         `json:"token"`
	ResetToken  sql.NullString `json:"reset_token"`
	Role        sql.NullString `json:"role"`
}
