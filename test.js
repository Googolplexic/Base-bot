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