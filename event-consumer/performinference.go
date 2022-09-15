package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"gocv.io/x/gocv"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
)

//seldon json payload
/*{
"data": {
	"names": [
"gender",

],
"ndarray": [
	[
		[]

	]
	       ]
		}
}
*/
type Data struct {
	Names   []string           `json:"names"`
	Ndarray [256][256][3]uint8 `json:"ndarray"`
}

type seldonpayload struct {
	Data `json:"data"`
}

//var (
//err   error
//frame *gocv.NativeByteBuffer
//)

//var skipcounter = 0

func PerformInference(imagedata []byte) {
	println("\nInferencing ....")
	//todo merge into one - not production ready
	unzippeddata, err := io.ReadAll(bytes.NewReader([]byte(imagedata)))
	if err != nil {
		fmt.Printf("Error in reading the decompressed byte array ... Ignoring..... %s\n", err)
		return
	}
	imagedataforinference, err := base64.StdEncoding.DecodeString(string(unzippeddata))
	if err != nil {
		fmt.Printf("Error in decoding the base6 array ... Ignoring..... %s\n", err)
		return
	}

	singedimarray := strings.Split(string(imagedataforinference), ",")
	const imagewidth = 255 * 4
	var imgarray [256][256][3]uint8
	for i := 0; i < 256; i++ {
		for j := 0; j < 256; j++ {
			firstitem := (i * (imagewidth)) + (j * 4)
			//imageData.data[( (50 * (imageData.width * 4) ) + (200 * 4)) + 2];

			imgarray[i][j][0] = str2int(singedimarray[firstitem])
			imgarray[i][j][1] = str2int(singedimarray[firstitem+1])
			imgarray[i][j][2] = str2int(singedimarray[firstitem+2])
		}
	}

	sp := newSeldonpayload(&Data{Names: []string{"image"}, Ndarray: imgarray})
	classification, err := postpayload(sp)
	go RecordClassification(classification)

}

func PerformInferenceFaster(imagedata []byte) {
	println("\nInferencing ....")
	//todo merge into one - not production ready
	var imagedataforinference []byte
	base64.StdEncoding.Decode(imagedataforinference, imagedata)

	/*	unzippeddata, err := io.ReadAll(bytes.NewReader([]byte(imagedata)))
		if err != nil {
			fmt.Printf("Error in reading the decompressed byte array ... Ignoring..... %s\n", err)
			return
		}
		imagedataforinference, err := base64.StdEncoding.DecodeString(string(unzippeddata))
		if err != nil {
			fmt.Printf("Error in decoding the base6 array ... Ignoring..... %s\n", err)
			return
		}
	*/
	singedimarray := strings.Split(string(imagedataforinference), ",")
	const imagewidth = 255 * 4
	var imgarray [256][256][3]uint8
	for i := 0; i < 256; i++ {
		for j := 0; j < 256; j++ {
			firstitem := (i * (imagewidth)) + (j * 4)
			//imageData.data[( (50 * (imageData.width * 4) ) + (200 * 4)) + 2];

			imgarray[i][j][0] = str2int(singedimarray[firstitem])
			imgarray[i][j][1] = str2int(singedimarray[firstitem+1])
			imgarray[i][j][2] = str2int(singedimarray[firstitem+2])
		}
	}

	sp := newSeldonpayload(&Data{Names: []string{"image"}, Ndarray: imgarray})
	classification, _ := postpayload(sp)
	go RecordClassification(classification)

}

func str2int(str string) uint8 {
	convertedint, err := strconv.Atoi(str)
	if err != nil {
		fmt.Printf("Error in conversion of string to int %s", err)
		return 0
	}
	return uint8(convertedint)
}
func PerformInferenceGoCV(imagedata []byte) {
	println("\nInferencing ....")
	img, err := gocv.IMDecode(imagedata, gocv.IMReadUnchanged)
	if err != nil {
		fmt.Printf("Exitting .. Failed to decode image: %s\n", err)
		os.Exit(1)
	}
	//skipcounter++
	//gocv.IMWrite("/tmp/"+strconv.Itoa(skipcounter)+".jpg", img)
	//fmt.Printf("size: %d x %d with %d channels \n", img.Rows(), img.Cols(), img.Channels())

	var imgarray [256][256][3]uint8
	bgr := gocv.Split(img)
	for i := 0; i < 256; i++ {
		for j := 0; j < 256; j++ {
			imgarray[i][j][0] = bgr[2].GetUCharAt(i, j)
			imgarray[i][j][1] = bgr[1].GetUCharAt(i, j)
			imgarray[i][j][2] = bgr[0].GetUCharAt(i, j)
		}
	}

	//fmt.Println(imgarray)

	// 	println("\n)))))))))))))))\n\n\n")

	sp := newSeldonpayload(&Data{Names: []string{"image"}, Ndarray: imgarray})
	classification, err := postpayload(sp)
	go RecordClassification(classification)
}

func postpayload(sp *seldonpayload) (string, error) {
	json, _ := json.Marshal(sp)
	// 	println(json)
	requestBody := bytes.NewBuffer(json)

	//"http://model-1-pred-demo-fmv3.apps.dbs-indo-1.apac-1.rht-labs.com/api/v1.0/predictions"
	modelUrl := os.Getenv("MODEL_URL")
	response, _ := http.Post(modelUrl, "application/json", requestBody)

	responsebody, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatalln(err.Error())
	}
	fmt.Printf(response.Status)
	body := string(responsebody)
	if strings.Contains(body, "Person") {
		fmt.Printf("\nPERSON\n")
		return "Person", nil
	} else if strings.Contains(body, "Background") {
		fmt.Printf("\nBACKGROUND\n")
		return "Background", nil
	} else if strings.Contains(body, "MidFinger") {
		fmt.Printf("\nMIDFINGER\n")
		return "MidFinger", nil
	}

	return "", errors.New("no classification found")

}
func newSeldonpayload(seldondata *Data) *seldonpayload {
	return &seldonpayload{Data: *seldondata}
}
