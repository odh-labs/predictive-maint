package main

import (
	"fmt"
	"gocv.io/x/gocv"
	"image"
	"log"
	// 	"strconv"
)

var (
	err    error
	webcam *gocv.VideoCapture
	frame  *gocv.NativeByteBuffer
)

var newsize = &image.Point{256, 256}

func FetchImages(ch chan<- gocv.NativeByteBuffer) {
	log.Println("Init Video Capture")
	webcam, err = gocv.VideoCaptureDevice(0)
	log.Println("VC Call completed")
	log.Println(err)
	if err != nil {
		fmt.Printf("Error opening capture device: \n")
		return
	}
	defer webcam.Close()

	processframes(ch)
}

func processframes(ch chan<- gocv.NativeByteBuffer) {
	var skipcounter = 0
	img := gocv.NewMat()
	defer img.Close()
	log.Println("Start VDO Captur eloop")
	for {

		if ok := webcam.Read(&img); !ok {
			fmt.Printf("Device closed\n")
			continue
		}
		//log.Println(" VDO Captur eloop .. Img Read")
		if img.Empty() {
			continue
		}

		skipcounter++
		if skipcounter%30 != 0 {
			//log.Println(" VDO Captur eloop .. Skip Counter ... miss 5 frames")
			continue
		}
		log.Println("VDO Capture Loop .... Resizing")

		go func() {
			//gocv.Resize(img, &img, image.Point{}, float64(0.5), float64(0.5), 0)
			gocv.Resize(img, &img, *newsize, 0, 0, 0)

			//this encoding can be moved at the consumer end
			frame, _ = gocv.IMEncode(".jpg", img)
			// 		gocv.IMWrite("/tmp/fm"+strconv.Itoa(skipcounter)+".jpg", img)
			log.Println("VDO Captur eLoop .... Pushing to channel")
			ch <- *frame

		}()
	}
}
