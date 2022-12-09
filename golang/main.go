package main

import (
	"strings"

	"github.com/SalomanYu/CleaningSkills/golang/db"
	"github.com/SalomanYu/CleaningSkills/golang/logger"
	"github.com/SalomanYu/CleaningSkills/golang/yandexapi"

)



func main(){
	skills := db.GetSkillFromRedis("without_banal")
	correctAllSkills(skills)
}

func correctAllSkills(skills []string) (correctedSlice []string) {
	for _, skill := range skills {
		correctedSkill := correct(skill)
		if correctedSkill != skill{
			db.SaveWrongVersionInRedis(db.WrongSkill{WrongVersion: skill, CorrectVersion:correctedSkill})
			db.SaveSkillAfterCorrectingGrammaticalErrors(correctedSkill)
			logger.Log.Printf("Ошибка - %s", correctedSkill)
		} else {
			db.SaveSkillAfterCorrectingGrammaticalErrors(skill)
			logger.Log.Printf("Нет ошибок - %s", skill)
		}
	}
	return 
}

func correct(skill string) (correctedSkill string) {
	correctedSkill = strings.Clone(skill)
	wrongWords := yandexapi.CheckText(skill)
	for _, word := range wrongWords {
		correctedSkill = strings.ReplaceAll(correctedSkill, word.WrongVersion, word.CorrectVersion[0])
	}
	return
}

func checkErr(err error) {
	if err != nil{
		panic(err)
	}
}