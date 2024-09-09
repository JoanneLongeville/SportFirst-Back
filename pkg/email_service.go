package pkg

import (
	"fmt"
	"net/smtp"
)

// EmailSender définit les paramètres nécessaires pour envoyer un email.
type EmailSender struct {
	SMTPHost    string
	SMTPPort    string
	SenderEmail string
	Auth        smtp.Auth
}

// NewEmailSender crée une instance de EmailSender.
func NewEmailSender(host, port, email string) *EmailSender {
	return &EmailSender{
		SMTPHost:    host,
		SMTPPort:    port,
		SenderEmail: email,
		Auth:        nil, // Pas d'authentification nécessaire pour MailHog
	}
}

// SendResetEmail envoie un email de réinitialisation de mot de passe.
func (es *EmailSender) SendResetEmail(to, resetLink string) error {
	subject := "Réinitialisation du mot de passe"
	body := fmt.Sprintf("Cliquez sur ce lien pour réinitialiser votre mot de passe: %s", resetLink)
	msg := []byte("To: " + to + "\r\n" +
		"From: " + es.SenderEmail + "\r\n" +
		"Subject: " + subject + "\r\n" +
		"\r\n" +
		body + "\r\n")

	smtpAddr := es.SMTPHost + ":" + es.SMTPPort
	return smtp.SendMail(smtpAddr, es.Auth, es.SenderEmail, []string{to}, msg)
}
