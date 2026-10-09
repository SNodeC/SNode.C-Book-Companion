#include "EchoServerFactory.h"

EchoServer* EchoServerFactory::create(web::websocket::SubProtocolContext* context) {
    return new EchoServer(context, getName());
}

extern "C" web::websocket::SubProtocolFactory<web::websocket::server::SubProtocol>*
echoServerSubProtocolFactory() {
    return new EchoServerFactory("echo");
}
