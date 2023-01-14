package model

import (
	"gorm.io/gorm"
)

type Actor struct {
	gorm.Model
	FirstName string `gorm:"not null" json:"first_name"`
	LastName  string `gorm:"not null" json:"last_name"`
	Age       int    `gorm:"not null" json:"age"`
	Gender    string `gorm:"not null" json:"gender"`
}
