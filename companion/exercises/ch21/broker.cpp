// A disposable local endpoint around the installed broker implementation.
#include <core/SNodeC.h>
#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <iot/mqtt/server/Mqtt.h>
#include <iot/mqtt/server/SocketContextFactory.h>
#include <net/in/stream/legacy/SocketServer.h>

class Factory final : public iot::mqtt::server::SocketContextFactory {
public:
    Factory()
        : iot::mqtt::server::SocketContextFactory("") {
    }

private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* connection,
           std::shared_ptr<iot::mqtt::server::broker::Broker> broker) override {
        return new iot::mqtt::SocketContext(
            connection,
            new iot::mqtt::server::Mqtt(connection->getConnectionName(), broker));
    }
};

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    const net::in::stream::legacy::SocketServer<Factory> broker("broker");
    broker.listen([](const auto&, const auto&) {
    });
    return core::SNodeC::start();
}
