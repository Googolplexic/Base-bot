var https = require('follow-redirects').https;
var fs = require('fs');

var options = {
    'method': 'GET',
    'hostname': 'v1.baseball.api-sports.io',
    'path': '/leagues',
    'headers': {
        'x-rapidapi-key': 'fe34cbe575f156400c9df830f52cedbc',
        'x-rapidapi-host': 'v1.baseball.api-sports.io'
    },
    'maxRedirects': 20
};

var req = https.request(options, function (res) {
    var chunks = [];

    res.on("data", function (chunk) {
        chunks.push(chunk);
    });

    res.on("end", function (chunk) {
        var body = Buffer.concat(chunks);
        console.log(body.toString());
    });

    res.on("error", function (error) {
        console.error(error);
    });
});

req.end();