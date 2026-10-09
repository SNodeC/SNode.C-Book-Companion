#include "EchoSocketContext.h"

#include <string>

EchoSocketContext::EchoSocketContext(
    core::socket::stream::SocketConnection* socketConnection, Role role)
    : core::socket::stream::SocketContext(socketConnection)
    , role(role) {
}

void EchoSocketContext::onConnected() {
    log().info() << "Echo context attached";

    if (role == Role::CLIENT) {
        sendToPeer("Hello peer! Nice to see you!!!");
    }
}

void EchoSocketContext::onDisconnected() {
    log().info("Echo context detached: {}",
               getDetachReason() == DetachReason::ContextSwitch ? "context switch"
                                                                : "connection close");
}

bool EchoSocketContext::onSignal([[maybe_unused]] int signum) {
    return true;
}

std::size_t EchoSocketContext::onReceivedFromPeer() {
    char chunk[4096];

    const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

    if (chunkLen > 0) {
        log().debug() << "Data to reflect: " << std::string(chunk, chunkLen);
        sendToPeer(chunk, chunkLen);
    }

    return chunkLen;
}

core::socket::stream::SocketContext* EchoServerSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection, EchoSocketContext::Role::SERVER);
}

core::socket::stream::SocketContext* EchoClientSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection, EchoSocketContext::Role::CLIENT);
}
