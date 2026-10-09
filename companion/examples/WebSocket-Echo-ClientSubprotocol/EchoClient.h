#ifndef SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_CLIENTSUBPROTOCOL_ECHOCLIENT_H
#define SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_CLIENTSUBPROTOCOL_ECHOCLIENT_H

#include <cstddef>
#include <cstdint>
#include <string>
#include <web/websocket/client/SubProtocol.h>

class EchoClient final : public web::websocket::client::SubProtocol {
public:
    EchoClient(web::websocket::SubProtocolContext* context, const std::string& name);

private:
    void onConnected() override;
    void onMessageStart(int opCode) override;
    void onMessageData(const char* chunk, std::size_t chunkLen) override;
    void onMessageEnd() override;
    void onMessageError(uint16_t errnum) override;
    void onDisconnected() override;
    bool onSignal(int sig) override;

    std::string currentMessage;
};

#endif
