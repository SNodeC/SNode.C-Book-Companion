#include "EchoServer.h"

#include <Log.h>
#include <web/websocket/SubProtocolContext.h>

EchoServer::EchoServer(web::websocket::SubProtocolContext* context,
                       const std::string& name)
    : web::websocket::server::SubProtocol(context, name, 90, 3) {
}

void EchoServer::onConnected() {
    snode::log::application().trace() << "WebSocket echo server connected";
}

void EchoServer::onMessageStart(int opCode) {
    currentMessageType = static_cast<std::uint8_t>(opCode);
    currentMessage.clear();
}

void EchoServer::onMessageData(const char* chunk, std::size_t chunkLen) {
    currentMessage.append(chunk, chunkLen);
}

void EchoServer::onMessageEnd() {
    snode::log::application().trace()
        << "WebSocket echo server received bytes: " << currentMessage.size();
    subProtocolContext->sendMessage(
        currentMessageType, currentMessage.data(), currentMessage.size());
}

void EchoServer::onMessageError(uint16_t errnum) {
    snode::log::application().warn() << "WebSocket echo server message error: " << errnum;
}

void EchoServer::onDisconnected() {
    snode::log::application().trace() << "WebSocket echo server disconnected";
}

bool EchoServer::onSignal(int) {
    sendClose();
    return false;
}
