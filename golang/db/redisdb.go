package db

import (
	"context"
	"os"
	"strings"
	"github.com/go-redis/redis/v9"
	"github.com/joho/godotenv"
)

func init(){
	err := godotenv.Load(".env")
	checkErr(err)
	
}

type WrongSkill struct{
	WrongVersion	string
	CorrectVersion	string 	
}


func GetSkillFromRedis(setName string) (values []string) {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
	})
	values, err := rdb.SMembers(ctx, setName).Result()
	checkErr(err) 
	return 
}

func SaveWrongVersionInRedis(coupleSkills WrongSkill) {
	// сохраняем в множестве редиса строку вида "неправильная версия|правильная версия"
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
	})
	value := strings.Join([]string{coupleSkills.WrongVersion, coupleSkills.CorrectVersion}, "|")
	err := rdb.SAdd(ctx, os.Getenv("SET_GRAMMATICAL_ERRORS"), value).Err()
	checkErr(err)
}


func SaveSkillAfterCorrectingGrammaticalErrors(skill string){
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
	})
	err := rdb.SAdd(ctx, os.Getenv("SET_GRAMMATICAL_CORRECTION"), skill).Err()
	checkErr(err)
}

func checkErr(err error) {
	if err != nil{
		panic(err)
	}
}