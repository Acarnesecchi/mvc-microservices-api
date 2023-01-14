package controller

import (
	"fmt"
	"github.com/Acarnesecchi/mvc-microservices-api/model"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
	"net/http"
	"strconv"
)

type ActorController struct {
	DB *gorm.DB
}

// Index action for actors
func (ac *ActorController) Index(w http.ResponseWriter, r *http.Request) {
	var actors []model.Actor
	ac.DB.Find(&actors)
	fmt.Fprintf(w, "All actors: %v", actors)
}

// Show action for actors
func (ac *ActorController) Show(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	id := r.URL.Query().Get("id")
	ac.DB.First(&actor, id)
	fmt.Fprintf(w, "Actor: %v", actor)
}

// Create action for actors
func (ac *ActorController) Create(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	r.ParseForm()
	actor.FirstName = r.FormValue("name")
	age, _ := strconv.Atoi(r.FormValue("age")) // convert string to int
	actor.Age = age
	ac.DB.Create(&actor)
	fmt.Fprintf(w, "Actor created: %v", actor)
}

// Update action for actors
func (ac *ActorController) Update(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	id := r.URL.Query().Get("id")
	ac.DB.First(&actor, id)
	r.ParseForm()
	actor.FirstName = r.FormValue("name")
	age, _ := strconv.Atoi(r.FormValue("age")) // convert string to int
	actor.Age = age
	ac.DB.Save(&actor)
	fmt.Fprintf(w, "Actor updated: %v", actor)
}

// Delete action for actors
func (ac *ActorController) Delete(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	id := r.URL.Query().Get("id")
	ac.DB.First(&actor, id)
	ac.DB.Delete(&actor)
	fmt.Fprintf(w, "Actor deleted")
}
