#include "SensorClient.h"

#include <core/SNodeC.h>
#include <core/socket/stream/SocketContextFactory.h>
#include <iot/mqtt/SocketContext.h>
#include <net/in/stream/legacy/SocketClient.h>

class Factory final : public core::socket::stream::SocketContextFactory {
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* connection) override {
        return new iot::mqtt::SocketContext(connection, new SensorClient);
    }
};

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    const net::in::stream::legacy::SocketClient<Factory> client("mqtt");
    client.connect([](const auto&, const auto&) {
    });
    return core::SNodeC::start();
}
