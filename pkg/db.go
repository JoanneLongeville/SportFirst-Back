package pkg

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/lib/pq"
	"gopkg.in/yaml.v3"
)

// Config structure pour les paramètres de la base de données.
type Config struct {
	Database struct {
		Host     string `yaml:"host"`
		Port     int    `yaml:"port"`
		User     string `yaml:"user"`
		Password string `yaml:"password"`
		DBName   string `yaml:"dbname"`
	} `yaml:"database"`
}

// NewDB crée et retourne une nouvelle connexion à la base de données.
func NewDB(configPath string) (*sql.DB, error) {
	var config Config

	// Lecture du fichier de configuration
	configFile, err := os.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("error reading config file: %v", err)
	}

	// Désérialisation du fichier de configuration
	err = yaml.Unmarshal(configFile, &config)
	if err != nil {
		return nil, fmt.Errorf("error unmarshaling config: %v", err)
	}

	// Création de la chaîne de connexion
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		config.Database.Host, config.Database.Port, config.Database.User, config.Database.Password, config.Database.DBName)

	// Tentative de connexion à la base de données
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %v", err)
	}

	// Vérification de la connexion
	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %v", err)
	}

	fmt.Println("Successfully connected to the database.")
	return db, nil
}
