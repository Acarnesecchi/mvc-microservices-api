package main

import (
	"actors/db"
	"fmt"
	"net/http"
)

func main() {
	db.DBConnection()
	defer db.DB.Close()
	// Migrate the schema
	db.DB.AutoMigrate(&Actor{})
	ac := &ActorController{DB: db.DB}
	SetupRoutes(ac)
	http.ListenAndServe(":8080", nil)
}
