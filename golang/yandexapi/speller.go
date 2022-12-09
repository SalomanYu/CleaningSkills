package yandexapi

import (
	"encoding/json"
	"net/http"
	"net/url"
	"io/ioutil"
	"io"

)

type WrongSkillJson struct{
	WrongVersion	string 		`json:"word"`
	CorrectVersion	[]string 	`json:"s"`
}

func CheckText(text string) (correctedSlice []WrongSkillJson) {
	generatedUrl := generateParamsUrl(text)
	req, err := http.Get(generatedUrl)
	checkErr(err)
	if req.StatusCode != 200{
		return
	}
	correctedSlice = parseJson(req.Body)
	return
}

func generateParamsUrl(paramsText string) (urlWithParams string) {
	params := url.Values{}
	params.Add("text", paramsText)
	params.Add("lang", "ru, en")
	urlWithParams = "https://speller.yandex.net/services/spellservice.json/checkText?" + params.Encode() 
	return 
}

func parseJson(data io.ReadCloser) (result []WrongSkillJson){	
	// распаковываем массив
	body, err := ioutil.ReadAll(data)
	checkErr(err)
    err = json.Unmarshal(body, &result)
	checkErr(err)
	return

}

func checkErr(err error) {
	if err != nil{
		panic(err)
	}
}