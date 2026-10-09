#include "SensorClient.h"

#include <iot/mqtt/client/SubProtocol.h>
#include <web/websocket/SubProtocolFactory.h>
#include <web/websocket/client/SubProtocolFactorySelector.h>

class Factory final
    : public web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol> {
public:
    Factory()
        : web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol>(
              "mqtt") {
    }

private:
    web::websocket::client::SubProtocol*
    create(web::websocket::SubProtocolContext* context) override {
        return new iot::mqtt::client::SubProtocol(context, getName(), new SensorClient);
    }
};
void linkMqttLab() {
    web::websocket::client::SubProtocolFactorySelector::link(
        "mqtt",
        +[]()
            -> web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol>* {
            return new Factory;
        });
}
