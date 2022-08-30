package main

import (
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"gocv.io/x/gocv"
	"log"
	"os"
)

var kch = make(chan kafka.Event, 5000)

var topic = "video-stream"

func initKafka() (*kafka.Producer, string, error) {
	hostname, err := os.Hostname()
	var kafkabroker = os.Getenv("KAFKA_BROKER_URL")
	if kafkabroker == "" {
		kafkabroker = "localhost:9092"
	}

	sasalusername := os.Getenv("CLIENT_ID")
	salpassword := os.Getenv("CLIENT_SECRET")

	//p, err := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": kafkabroker,
	//	"client.id": hostname,
	//	"acks":      "0"})

	p, err := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": kafkabroker,
		"client.id":         hostname,
		"acks":              "1",
		"sasl.mechanism":    "PLAIN",
		"security.protocol": "SASL_SSL",
		"sasl.username":     sasalusername,
		"sasl.password":     salpassword})

	if err != nil {
		println(err.Error())
		os.Exit(1)
	}
	return p, hostname, err

}

func Push(ch <-chan gocv.NativeByteBuffer) {
	p, hostname, err := initKafka()
	if err != nil {
		fmt.Printf("Exitting .. Failed to create producer: %s\n", err)
		os.Exit(1)
	}

	//go func() {
	//	for e := range p.Events() {
	//		switch ev := e.(type) {
	//		case *kafka.Message:
	//			if ev.TopicPartition.Error != nil {
	//				fmt.Printf("Failed to deliver message: %v\n", ev.TopicPartition)
	//			} else {
	//				fmt.Printf("Successfully produced record to topic %s partition [%d] @ offset %v\n",
	//					*ev.TopicPartition.Topic, ev.TopicPartition.Partition, ev.TopicPartition.Offset)
	//			}
	//		}
	//	}
	//}()

	for frame := range ch {
		log.Println("Received frame and pushing to Kafka")
		log.Println(frame.Len())
		//log.Println(frame.GetBytes())

		err = p.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic},
			Value:          frame.GetBytes(),
			Key:            []byte(hostname)},
			kch,
		)

		if err != nil {
			println("Push UNSUCCESSFULL")
			println(err.Error())
		}

	}
}
