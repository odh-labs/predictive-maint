package main

import (
	"gocv.io/x/gocv"
	"log"
	"sync"
)

var wg sync.WaitGroup

func main() {
	ch := make(chan gocv.NativeByteBuffer, 5000)
	defer close(ch)

	wg.Add(2)

	//fetch video stream
	log.Println("Init Camera")
	go func() {
		defer wg.Done()
		FetchImages(ch)
	}()

	//Send events
	log.Println("Init Message push")
	go func() {
		defer wg.Done()
		Push(ch)
	}()

	log.Println("Waiting ...")
	wg.Wait()
}
