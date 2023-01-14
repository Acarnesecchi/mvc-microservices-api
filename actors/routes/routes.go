package main

import (
	"github.com/Acarnesecchi/mvc-microservices-api/controller"
	"net/http"
)

func SetupRoutes(ac controller.ActorController) {
	http.HandleFunc("/actors", ac.Index)
	http.HandleFunc("/actors/show", ac.Show)
	http.HandleFunc("/actors/create", ac.Create)
	http.HandleFunc("/actors/update", ac.Update)
	http.HandleFunc("/actors/delete", ac.Delete)
}
