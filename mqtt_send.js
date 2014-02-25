var rpc = require('./amqp-rpc/amqp_rpc');
var amqp = require('./amqp-rpc/node_modules/amqplib');

var log = function(msg){
    process.stdout.write("test::amqp_rpc.js: ");
    console.log (msg);
}

var mqServerUrl = 'amqp://onionCore:p@mqtt.onion.io';
var open = amqp.connect(mqServerUrl);

rpc.register('IF_MQTT_SEND', function(params, callback){
    var key = '.'+params.deviceId
    var cmd = params.cmd.toString()
    log(key);

    open.then(function(conn) {
        conn.createChannel().then(function(ch) {
            ch.publish('amq.topic', key, new Buffer(cmd));
            ch.close();
        });
    });

    log(params);

    callback({});
});


