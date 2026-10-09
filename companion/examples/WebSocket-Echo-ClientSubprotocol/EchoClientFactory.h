#ifndef SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_CLIENTSUBPROTOCOL_ECHOCLIENTFACTORY_H
#define SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_CLIENTSUBPROTOCOL_ECHOCLIENTFACTORY_H

#include "EchoClient.h"

#include <web/websocket/SubProtocolFactory.h>
#include <web/websocket/client/SubProtocol.h>

class EchoClientFactory final
    : public web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol> {
public:
    using web::websocket::SubProtocolFactory<
        web::websocket::client::SubProtocol>::SubProtocolFactory;

private:
    EchoClient* create(web::websocket::SubProtocolContext* context) override;
};

extern "C" web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol>*
echoClientSubProtocolFactory();

#endif
