package routes

import (
	"actors/controller"
	"github.com/gorilla/mux"
)

func SetupRoutes(ac controller.ActorController, router *mux.Router) {
	router.HandleFunc("/actors", ac.Index).Methods("GET")
	router.HandleFunc("/actors/create", ac.Create).Methods("POST")
	router.HandleFunc("/actors/{id:[0-9]+}", ac.Update).Methods("PUT")
	router.HandleFunc("/actors/{id:[0-9]+}", ac.Delete).Methods("DELETE")
	router.HandleFunc("/actors/{id:[0-9]+}", ac.Show).Methods("GET")
}
