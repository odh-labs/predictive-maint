#FROM denismakogon/gocv-alpine:4.0.1-buildstage as builder
FROM registry.fedoraproject.org/fedora:36 as builder

LABEL version="1.0" \
      maintainer="fmasood@redhat.com"

RUN dnf -y install opencv opencv-contrib opencv-devel go librdkafka librdkafka-devel git gcc g++
RUN mkdir -p /go/src/app && dnf -y update
COPY ./*.go ./go.* /go/src/app/

WORKDIR /go/src/app

RUN GO111MODULE=on go mod download -x
RUN GO111MODULE=on CGO_ENABLED=1 GOOS=linux go build -tags static_all -gcflags="-e" -a -installsuffix cgo -o main .


FROM registry.fedoraproject.org/fedora:36
RUN dnf -y install opencv opencv-contrib librdkafka librdkafka-devel
COPY --from=builder /go/src/app/main /app/
WORKDIR /app
USER 1001
CMD ["./main"]