#include "EchoClient.h"

#include <Log.h>

EchoClient::EchoClient(web::websocket::SubProtocolContext* context,
                       const std::string& name)
    : web::websocket::client::SubProtocol(context, name, 90, 3) {
}

void EchoClient::onConnected() {
    snode::log::application().trace() << "WebSocket echo client connected";
    sendMessage("hello");
}

void EchoClient::onMessageStart(int) {
    currentMessage.clear();
}

void EchoClient::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoClient::onMessageEnd() {
    snode::log::application().trace()
        << "WebSocket echo client received: " << currentMessage;
    currentMessage.clear();
    sendClose();
}

void EchoClient::onMessageError(uint16_t errnum) {
    snode::log::application().warn() << "WebSocket echo client message error: " << errnum;
    currentMessage.clear();
}

void EchoClient::onDisconnected() {
    snode::log::application().trace() << "WebSocket echo client disconnected";
    currentMessage.clear();
}

bool EchoClient::onSignal(int) {
    sendClose();
    return false;
}
