package main

import (
	"context"
	"fmt"
	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/push"
	"gocv.io/x/gocv"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"sync/atomic"
	"time"
)

func RecordClassification(img gocv.Mat, classification string) {

	//publishToPrometheus(img, classification)
	publishToS3(img, classification)

}

var background_count_s3 int32 = 0
var person_count_s3 int32 = 0
var Finger_count_s3 int32 = 0

func publishToS3(img gocv.Mat, classification string) {
	endpoint := os.Getenv("MINIO_SERVER")
	accessKeyID := os.Getenv("MINIO_USER")
	secretAccessKey := os.Getenv("MINIO_PASSWORD")
	useSSL := false

	// Initialize minio client object.
	minioClient, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKeyID, secretAccessKey, ""),
		Secure: useSSL,
	})
	if err != nil {
		log.Fatalln(err)
	}

	//var file *bytes.Buffer
	var file int32

	if classification == "Person" {
		atomic.AddInt32(&person_count_s3, 1)
		file = person_count_s3
	} else if classification == "Background" {
		atomic.AddInt32(&background_count_s3, 1)
		file = background_count_s3
	} else if classification == "Finger" {
		atomic.AddInt32(&Finger_count_s3, 1)
		file = Finger_count_s3
	}
	//println(strconv.Itoa(int(file)))
	//println("file is formed")
	//put update data
	filereader := strings.NewReader(strconv.Itoa(int(file)))
	_, err = minioClient.PutObject(context.Background(), "image-prediction", classification+".txt",
		filereader, int64(filereader.Len()),
		minio.PutObjectOptions{ContentType: "text/plain"})

	//put an image
	//file = bytes.NewBufferString()
	//_, err = minioClient.PutObject(context.Background(), "image-prediction", randomString(16),
	//	file, int64(file.Len()),
	//	minio.PutObjectOptions{ContentType: "application/octet-stream"})

	//gocv.IMWrite("/tmp/dyn.jpg", img)
	//_, err = minioClient.FPutObject(context.Background(), "image-prediction", "file",
	//	"a.jpg", minio.PutObjectOptions{ContentType: "application/octet-stream"})

	if err != nil {
		println("Error PutObject")
		println(err.Error())
	}
}

var promserver = os.Getenv("PROMETHEUS_SERVER")

var (
	person_count = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "Person",
		Help: "Total number of person detected",
	})

	background_count = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "Background",
		Help: "Total number of background detected",
	})

	Finger_count = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "Finger",
		Help: "Total number of Finger detected",
	})
)

func publishToPrometheus(img gocv.Mat, classification string) {
	var counter prometheus.Collector

	if classification == "Person" {
		person_count.Inc()
		counter = person_count
	} else if classification == "Background" {
		background_count.Inc()
		counter = background_count
	} else if classification == "Finger" {
		Finger_count.Inc()
		counter = Finger_count
	}
	err := push.New(promserver, "pred_maint_job").
		Collector(counter).
		Grouping("pred_maint", "customers").
		Push()

	if err != nil {
		fmt.Printf(err.Error())
		fmt.Printf("Error in pushing to prometheus")
	}
}

func randomString(length int) string {
	rand.Seed(time.Now().UnixNano())
	b := make([]byte, length)
	rand.Read(b)
	return fmt.Sprintf("%x", b)[:length]
}
