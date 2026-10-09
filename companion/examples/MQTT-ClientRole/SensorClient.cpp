#include "SensorClient.h"

#include <Log.h>

SensorClient::SensorClient()
    : iot::mqtt::client::Mqtt(
          "sensor-mqtt", "sensor-client-1", 60, "sensor-client.session") {
}

void SensorClient::onConnected() {
    sendConnect(true, "", "", 0, false, "", "", false);
}

void SensorClient::onConnack(const iot::mqtt::packets::Connack&) {
    sendSubscribe({
        iot::mqtt::Topic("sensors/+/command", 0),
    });

    sendPublish("sensors/temperature/value", "23.5", 0, false);
}

void SensorClient::onPublish(const iot::mqtt::packets::Publish& publish) {
    const std::string topic = publish.getTopic();
    const std::string message = publish.getMessage();

    snode::log::application().trace() << "MQTT command on " << topic << ": " << message;
}

bool SensorClient::onSignal(int) {
    sendDisconnect();
    return false;
}
