package db

import (
	"fmt"
	"github.com/spf13/viper"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
)

var DB *gorm.DB

func DBConnection() {
	viper.AddConfigPath("db")
	viper.SetConfigName("database_local")
	viper.SetConfigType("ini")
	//viper.SetConfigName("database")
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatal("Error reading config file, %s", err)
	}

	host := viper.GetString("postgresql.host")
	port := viper.GetInt("postgresql.port")
	user := viper.GetString("postgresql.user")
	password := viper.GetString("postgresql.password")
	dbName := viper.GetString("postgresql.database")

	connect := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbName)

	DB, err = gorm.Open(postgres.Open(connect), &gorm.Config{})
	if err != nil {
		log.Fatal("Error connecting to database, %s", err)
	}
}
