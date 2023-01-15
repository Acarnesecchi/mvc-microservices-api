package main

import (
	"actors/controller"
	"actors/db"
	"actors/model"
	"actors/routes"
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func main() {
	db.DBConnection()
	log.Println("Database connected")
	db.DB.AutoMigrate(&model.Actor{})
	ac := controller.ActorController{DB: db.DB}
	router := mux.NewRouter().StrictSlash(true)
	routes.SetupRoutes(ac, router)
	log.Println("Listening on port 8080")
	http.ListenAndServe(":8080", router)
}
