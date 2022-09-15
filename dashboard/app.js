var log = require('console-log-level')({ prefix: function (level) {
    return level + ' ' + new Date().toISOString()
  },
  level: process.argv[3] || 'info'  });
var http = require("http"),
    url = require("url"),
    path = require("path"),
    fs = require("fs"),
    axios = require('axios');

   
var MINIO_URL = process.env.MINIO_URL;

process.on('SIGINT', function() {
    process.exit();
});

http.createServer( function(request, response) {
    var pathname = url.parse(request.url).pathname;

    if (pathname.startsWith("/minio/")) {
        var minioURL = MINIO_URL + pathname.substring(6);
        log.info(minioURL);

        axios.get(minioURL, {responseType: "text",})
        .then(function (res) {
          // handle success
          log.debug(res.data);
          response.statusCode =res.status;
          response.setHeader("Content-Type", res.headers["content-type"]);
          var buf = Buffer.from(res.data.toString(), 'utf8');
          response.write(buf);
          response.end();
        })
        .catch(function (error) {
          // handle error
          console.log(error);
          log.error('problem with request: ${e.message}');
          response.writeHead(500, {"Content-Type": "text/plain"});
          response.write(error + "\n");
          response.end();
          return;
        })

    } else {
		var uri = url.parse(request.url).pathname
			, filename = path.join(process.cwd(), uri);

		fs.exists(filename, function(exists) {
			if(!exists) {
                response.writeHead(404, {"Content-Type": "text/plain"});
                response.write("404 Not Found\n");
                response.end();
                return;
			}
		
			if (fs.statSync(filename).isDirectory()) filename += '/index.html';
		
			fs.readFile(filename, "binary", function(err, file) {
				if(err) {        
					response.writeHead(500, {"Content-Type": "text/plain"});
					response.write(err + "\n");
					response.end();
					return;
				}

				response.writeHead(200);
				response.write(file, "binary");
				response.end();
			});
	
  		});
  	}
}).listen(parseInt(8080, 10));