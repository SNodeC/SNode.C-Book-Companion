#ifndef SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_CLIENT_LINECOMMANDCLIENTCONTEXTFACTORY_H
#define SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_CLIENT_LINECOMMANDCLIENTCONTEXTFACTORY_H

#include "LineCommandClientContext.h"

#include <core/socket/stream/SocketContextFactory.h>

class LineCommandClientContextFactory final
    : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override {
        return new LineCommandClientContext(socketConnection);
    }
};

#endif
