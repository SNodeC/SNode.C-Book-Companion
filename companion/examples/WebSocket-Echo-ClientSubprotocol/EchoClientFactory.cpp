#include "EchoClientFactory.h"

EchoClient* EchoClientFactory::create(web::websocket::SubProtocolContext* context) {
    return new EchoClient(context, getName());
}

extern "C" web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol>*
echoClientSubProtocolFactory() {
    return new EchoClientFactory("echo");
}
