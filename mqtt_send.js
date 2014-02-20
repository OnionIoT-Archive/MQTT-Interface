var rpc = require('./amqp-rpc/amqp_rpc');
var amqp = require('./amqp-rpc/node_modules/amqplib');

var log = function(msg){
    process.stdout.write("test::amqp_rpc.js: ");
    console.log (msg);
}

var mqServerUrl = 'amqp://onionCore:p@mqtt.onion.io';
var conn = null;
var open = amqp.connect(mqServerUrl);
open.then(function(connection) {
    log('mqtt connection opened');
    conn = connection;
});



rpc.register('IF_MQTT_SEND', function(params, callback){
    var deviceId = params.deviceId
    var cmd = params.cmd.toString()

    open.then(function(conn) {
        conn.createChannel().then(function(ch) {
            ch.publish('amq.topic', '.'+deviceId, cmd);
        });
    });

    console.log(params);

    callback({});
});


