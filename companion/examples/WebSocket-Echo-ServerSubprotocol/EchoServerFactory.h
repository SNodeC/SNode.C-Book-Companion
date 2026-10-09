#ifndef SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_SERVERSUBPROTOCOL_ECHOSERVERFACTORY_H
#define SNODEC_BOOK_EXAMPLES_WEBSOCKET_ECHO_SERVERSUBPROTOCOL_ECHOSERVERFACTORY_H

#include "EchoServer.h"

#include <web/websocket/SubProtocolFactory.h>
#include <web/websocket/server/SubProtocol.h>

class EchoServerFactory final
    : public web::websocket::SubProtocolFactory<web::websocket::server::SubProtocol> {
public:
    using web::websocket::SubProtocolFactory<
        web::websocket::server::SubProtocol>::SubProtocolFactory;

private:
    EchoServer* create(web::websocket::SubProtocolContext* context) override;
};

extern "C" web::websocket::SubProtocolFactory<web::websocket::server::SubProtocol>*
echoServerSubProtocolFactory();

#endif
