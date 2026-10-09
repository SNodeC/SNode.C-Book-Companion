#ifndef ECHO_SOCKET_CONTEXT_H
#define ECHO_SOCKET_CONTEXT_H

#include <core/socket/stream/SocketContext.h>
#include <core/socket/stream/SocketContextFactory.h>
#include <cstddef>

namespace core::socket::stream {
    class SocketConnection;
}

class EchoSocketContext : public core::socket::stream::SocketContext {
public:
    enum class Role { SERVER, CLIENT };

    explicit EchoSocketContext(core::socket::stream::SocketConnection* socketConnection,
                               Role role);

private:
    void onConnected() override;
    void onDisconnected() override;
    bool onSignal(int signum) override;
    std::size_t onReceivedFromPeer() override;

    Role role;
};

class EchoServerSocketContextFactory : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override;
};

class EchoClientSocketContextFactory : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override;
};

#endif
