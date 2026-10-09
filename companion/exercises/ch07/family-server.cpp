#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <core/socket/stream/SocketConnection.h>
#include LAB_HEADER
#include <iostream>

// Each target selects one carrier; the canonical context/factory is unchanged.
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    using Server =
        net::LAB_FAMILY::stream::legacy::SocketServer<EchoServerSocketContextFactory>;
    Server server("endpoint");
    server.setOnConnected([](core::socket::stream::SocketConnection* connection) {
        // Copy observations while this borrowed connection pointer is valid.
        std::cerr << "IDENTITY\t" << connection->getLocalAddress().toString() << '\t'
                  << connection->getRemoteAddress().toString() << std::endl;
    });
    server.listen(
        [](const Server::SocketAddress& address, const core::socket::State& state) {
            if (state == core::socket::State::OK) {
                std::cout << "BOUND\t" << address.toString() << std::endl;
            } else {
                std::cerr << "STATUS\t" << state.what() << std::endl;
            }
        });
    return core::SNodeC::start();
}
