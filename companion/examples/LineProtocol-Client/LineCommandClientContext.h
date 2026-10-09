#ifndef SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_CLIENT_LINECOMMANDCLIENTCONTEXT_H
#define SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_CLIENT_LINECOMMANDCLIENTCONTEXT_H

#include <core/socket/stream/SocketContext.h>
#include <cstddef>
#include <string>

namespace core::socket::stream {
    class SocketConnection;
}

class LineCommandClientContext final : public core::socket::stream::SocketContext {
public:
    explicit LineCommandClientContext(
        core::socket::stream::SocketConnection* socketConnection);

private:
    void onConnected() override;
    void onDisconnected() override;
    bool onSignal(int signum) override;
    std::size_t onReceivedFromPeer() override;

    void processLine(const std::string& line);
    void sendNextCommand();

    std::string receiveBuffer;
    bool readyReceived = false;
    std::size_t nextCommandIndex = 0;
};

#endif
