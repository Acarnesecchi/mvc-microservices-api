package controller

import (
	"actors/model"
	"encoding/json"
	"github.com/gorilla/mux"
	_ "gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"net/http"
	"os"
	"strconv"
)

type ActorController struct {
	DB *gorm.DB
}
type Actor struct {
	ID          uint   `json:"id"`
	First_Name  string `json:"first_name"`
	Second_Name string `json:"second_name"`
	Age         int    `json:"age"`
	Gender      string `json:"gender"`
}

func logger(logMessage string) {
	logfile, err := os.OpenFile("logfile.txt", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	defer logfile.Close()

	log.SetOutput(logfile)
	log.Println(logMessage)
}

var URL_MOVIES = "http://localhost:5000/movies"

func (ac *ActorController) Index(w http.ResponseWriter, r *http.Request) {
	var actors []model.Actor
	ac.DB.Find(&actors)
	var filteredActors []Actor
	for _, a := range actors {
		filteredActors = append(filteredActors, Actor{
			ID:          a.ID,
			First_Name:  a.First_Name,
			Second_Name: a.Second_Name,
			Age:         a.Age,
			Gender:      a.Gender,
		})
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(filteredActors)
}

func (ac *ActorController) Show(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	vars := mux.Vars(r)
	id := vars["id"]
	ac.DB.First(&actor, id)
	actorJson := Actor{ID: actor.ID, First_Name: actor.First_Name, Second_Name: actor.Second_Name, Age: actor.Age, Gender: actor.Gender}
	if actor.ID == 0 {
		json.NewEncoder(w).Encode("Actor not found")
		logger("Failed to find actor with id: " + id)
		return
	}

	logger("Found actor with id: " + id)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(actorJson)
}

func (ac *ActorController) Create(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	r.ParseForm()
	actor.First_Name = r.FormValue("first_name")
	actor.Second_Name = r.FormValue("second_name")
	age, _ := strconv.Atoi(r.FormValue("age"))
	actor.Age = age
	actor.Gender = r.FormValue("gender")
	ac.DB.Create(&actor)
	logger("Created actor with name: " + actor.First_Name + " " + actor.Second_Name)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(actor)
}

func (ac *ActorController) Update(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	id := mux.Vars(r)["id"]
	err := ac.DB.First(&actor, "id = ?", id).Error
	if err == gorm.ErrRecordNotFound {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(map[string]string{"error": "you suck"})
		logger("Failed to find actor with id: " + id)
		return
	}
	r.ParseForm()
	actor.First_Name = r.FormValue("first_name")
	actor.Second_Name = r.FormValue("second_name")
	age, _ := strconv.Atoi(r.FormValue("age"))
	actor.Age = age
	actor.Gender = r.FormValue("gender")
	ac.DB.Save(&actor)
	logger("Updated actor with id: " + id)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(actor)
}

func (ac *ActorController) Delete(w http.ResponseWriter, r *http.Request) {
	var actor model.Actor
	id := mux.Vars(r)["id"]
	ac.DB.First(&actor, "id = ?", id)
	if actor.ID == 0 {
		json.NewEncoder(w).Encode(map[string]string{"error": "you suck"})
		logger("Failed to find actor with id: " + id)
		return
	}
	ac.DB.Delete(&actor)
	logger("Deleted actor with id: " + id)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode("Actor deleted")
}
