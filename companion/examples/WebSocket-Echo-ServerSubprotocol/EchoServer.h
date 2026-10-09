#ifndef SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_SERVERSUBPROTOCOL_ECHOSERVER_H
#define SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_SERVERSUBPROTOCOL_ECHOSERVER_H

#include <cstddef>
#include <cstdint>
#include <string>
#include <web/websocket/server/SubProtocol.h>

class EchoServer final : public web::websocket::server::SubProtocol {
public:
    EchoServer(web::websocket::SubProtocolContext* context, const std::string& name);

private:
    void onConnected() override;
    void onMessageStart(int opCode) override;
    void onMessageData(const char* chunk, std::size_t chunkLen) override;
    void onMessageEnd() override;
    void onMessageError(uint16_t errnum) override;
    void onDisconnected() override;
    bool onSignal(int sig) override;

    std::uint8_t currentMessageType = 0;
    std::string currentMessage;
};

#endif
