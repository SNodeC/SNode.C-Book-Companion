#include "LineCommandServerContext.h"

#include <Log.h>
#include <core/socket/SocketAddress.h>
#include <core/socket/stream/SocketConnection.h>
#include <string>

LineCommandServerContext::LineCommandServerContext(
    core::socket::stream::SocketConnection* socketConnection)
    : core::socket::stream::SocketContext(socketConnection) {
}

void LineCommandServerContext::onConnected() {
    snode::log::application().trace()
        << "Line command server connected to "
        << getSocketConnection()->getRemoteAddress().toString();
    sendToPeer("READY\n");
}

void LineCommandServerContext::onDisconnected() {
    snode::log::application().trace()
        << "Line command server disconnected from "
        << getSocketConnection()->getRemoteAddress().toString();
    receiveBuffer.clear();
}

bool LineCommandServerContext::onSignal(int signum) {
    snode::log::application().trace()
        << "Line command server closing due to signal " << signum;
    close();

    return true;
}

std::size_t LineCommandServerContext::onReceivedFromPeer() {
    char chunk[1024];
    const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

    if (chunkLen > 0) {
        receiveBuffer.append(chunk, chunkLen);

        std::size_t lineEnd = receiveBuffer.find('\n');
        while (lineEnd != std::string::npos && lineEnd <= maxLineLength) {
            std::string line = receiveBuffer.substr(0, lineEnd);
            if (!line.empty() && line.back() == '\r') {
                line.pop_back();
            }

            if (!processLine(line)) {
                receiveBuffer.clear();
                return chunkLen;
            }
            receiveBuffer.erase(0, lineEnd + 1);
            lineEnd = receiveBuffer.find('\n');
        }

        if (receiveBuffer.length() > maxLineLength) {
            snode::log::application().warn()
                << "Line command server closing after overlong pending line";
            sendToPeer("ERR line too long\n");
            receiveBuffer.clear();
            close();
        }
    }

    return chunkLen;
}

bool LineCommandServerContext::processLine(const std::string& line) {
    if (!line.empty()) {
        snode::log::application().trace()
            << "Line command server received '" << line << "'";

        if (line == "PING") {
            sendToPeer("PONG\n");
        } else if (line == "STATUS") {
            sendToPeer("OK\n");
        } else if (line == "QUIT") {
            close();
            return false;
        } else {
            sendToPeer("ERR unknown command\n");
        }
    }
    return true;
}
