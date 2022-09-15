const { Kafka } = require('kafkajs');
const http = require("http");
const { CompressionTypes } = require('kafkajs');
const url = require("url");
const path = require("path");
const fs = require("fs");

var CAPTURE_INTERVAL = 1200;
if (process.env.CAPTURE_INTERVAL) {
  CAPTURE_INTERVAL = process.env.CAPTURE_INTERVAL;
}

console.log(process.env.KAFKA_BROKER_URL)

const kafka = new Kafka({
  clientId: 'video-topic',
    brokers: [process.env.KAFKA_BROKER_URL],
  ssl: true,
  logLevel: 2,
 sasl: {
   mechanism: 'plain',
   username: process.env.SASL_USERNAME,
   password: process.env.SASL_PASSWORD
 }
})

process.on('SIGINT', function() {
  process.exit();
});

var isConnected = false

const producer = kafka.producer()
producer.on('producer.connect', () => {
  console.log(`KafkaProvider: connected`);
  isConnected = true
});
producer.on('producer.disconnect', () => {
  console.log(`KafkaProvider: could not connect`);
});
producer.on('producer.network.request_timeout', (payload) => {
  console.log(`KafkaProvider: request timeout ${payload.clientId}`);
});
const run = async () => {
  // Producing
  await producer.connect()
}

const host = '0.0.0.0';
const port = 8080;


const requestListener = async function (req, res) {
  var pathname = url.parse(req.url).pathname;
  if (pathname.startsWith("/send")) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Request-Method', '*');
    res.setHeader('Access-Control-Allow-Methods', 'OPTIONS, POST');
    res.setHeader('Access-Control-Allow-Headers', '*');
    if ( req.method === 'OPTIONS' ) {
      res.writeHead(200);
      res.end();
      return;
    }

    if (!isConnected){
      console.log('message NOT posted becuase server is still connecting ' + new Date());
      res.writeHead(200)
      res.end();

    }

//    console.log(req)
    var body = "";
      req.on('data', function (chunk) {
        body += chunk;
      });
      req.on('end', function () {
//        console.log('\n\n\n***body: ' + body);
//        var jsonObj = JSON.parse(body);
//      console.log(jsonObj.test);
        producer.send({
        topic: 'video-stream',
        compression: CompressionTypes.GZIP,
        messages: [
          {
            value: Buffer.from(body)
          },
        ],
      });
              console.log('message posted at ' + new Date());
      res.writeHead(200)
      res.end();

      })
    } else {
      var uri = url.parse(req.url).pathname
        , filename = path.join(process.cwd(), uri);
  
      fs.exists(filename, function(exists) {
        if(!exists) {
          res.writeHead(404, {"Content-Type": "text/plain"});
          res.write("404 Not Found\n");
          res.end();
                  return;
        }
      
        if (fs.statSync(filename).isDirectory()) filename += '/index.html';
      
        fs.readFile(filename, "binary", function(err, file) {
          if(err) {        
            res.writeHead(500, {"Content-Type": "text/plain"});
            res.write(err + "\n");
            res.end();
            return;
          }
  
          res.writeHead(200);
          res.write(file, "binary");
          res.end();
        });
    
        });
    }

};

run().catch(console.error)


const server = http.createServer(requestListener);
server.listen(port, () => {
    console.log(`Server is running on http://${host}:${port}`);
});


