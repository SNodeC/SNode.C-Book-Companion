#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <net/in/stream/legacy/SocketClient.h>

class GreetingContext : public EchoSocketContext {
public:
    explicit GreetingContext(core::socket::stream::SocketConnection* connection)
        : EchoSocketContext(connection, Role::CLIENT) {
    }

private:
    void onConnected() override {
        sendToPeer("Learning by echo");
    }
};

class GreetingFactory : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* connection) override {
        return new GreetingContext(connection);
    }
};

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    using Client = net::in::stream::legacy::SocketClient<GreetingFactory>;
    Client client("greeting-client");
    client.connect(
        "127.0.0.1", 8080, [](const Client::SocketAddress&, const core::socket::State&) {
        });
    return core::SNodeC::start();
}
