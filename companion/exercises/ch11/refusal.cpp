#include "LineCommandServerContextFactory.h"

#include <core/SNodeC.h>
#include <net/in/stream/legacy/SocketServer.h>

// Test-only construction policy; protocol and ordinary creation stay canonical.
class RefuseFirst final : public core::socket::stream::SocketContextFactory {
    bool first = true;
    LineCommandServerContextFactory accepted;
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* connection) override {
        if (first) {
            first = false;
            return nullptr;
        }
        return static_cast<core::socket::stream::SocketContextFactory&>(accepted).create(
            connection);
    }
};

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    using Server = net::in::stream::legacy::SocketServer<RefuseFirst>;
    Server server("lineprotocolserver");
    server.listen([](const Server::SocketAddress&, const core::socket::State&) {
    });
    return core::SNodeC::start();
}
