#ifndef SNODEC_BOOK_EXAMPLES_MQTT_CLIENTROLE_SENSORCLIENT_H
#define SNODEC_BOOK_EXAMPLES_MQTT_CLIENTROLE_SENSORCLIENT_H

#include <iot/mqtt/Topic.h>
#include <iot/mqtt/client/Mqtt.h>
#include <iot/mqtt/packets/Connack.h>
#include <iot/mqtt/packets/Publish.h>

class SensorClient final : public iot::mqtt::client::Mqtt {
public:
    SensorClient();

private:
    void onConnected() override;
    void onConnack(const iot::mqtt::packets::Connack& connack) override;
    void onPublish(const iot::mqtt::packets::Publish& publish) override;
    bool onSignal(int sig) override;
};

#endif
