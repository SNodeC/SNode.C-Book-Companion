#ifndef SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_SERVER_LINECOMMANDSERVERCONTEXT_H
#define SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_SERVER_LINECOMMANDSERVERCONTEXT_H

#include <core/socket/stream/SocketContext.h>
#include <cstddef>
#include <string>

namespace core::socket::stream {
    class SocketConnection;
}

class LineCommandServerContext final : public core::socket::stream::SocketContext {
public:
    explicit LineCommandServerContext(
        core::socket::stream::SocketConnection* socketConnection);

private:
    static constexpr std::size_t maxLineLength = 4096;

    void onConnected() override;
    void onDisconnected() override;
    bool onSignal(int signum) override;
    std::size_t onReceivedFromPeer() override;

    bool processLine(const std::string& line);

    std::string receiveBuffer;
};

#endif
