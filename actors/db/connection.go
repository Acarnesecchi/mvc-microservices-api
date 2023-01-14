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
	viper.SetConfigName("ini")
	//viper.AddConfigPath("database")
	viper.AddConfigPath("database_local")
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatal("Error reading config file, %s", err)
	}

	host := viper.GetString("database.host")
	port := viper.GetInt("database.port")
	user := viper.GetString("database.user")
	password := viper.GetString("database.password")
	dbName := viper.GetString("database.dbname")

	connect := fmt.Sprintf("host=%s port=%d user=%s password=%s dbName=%s sslmode=disable",
		host, port, user, password, dbName)

	DB, err = gorm.Open(postgres.Open(connect), &gorm.Config{})
	if err != nil {
		log.Fatal("Error connecting to database, %s", err)
	}
}
