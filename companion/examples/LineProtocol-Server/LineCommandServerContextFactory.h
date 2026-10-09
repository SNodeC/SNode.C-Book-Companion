#ifndef SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_SERVER_LINECOMMANDSERVERCONTEXTFACTORY_H
#define SNODEC_BOOK_EXAMPLES_LINEPROTOCOL_SERVER_LINECOMMANDSERVERCONTEXTFACTORY_H

#include "LineCommandServerContext.h"

#include <core/socket/stream/SocketContextFactory.h>

class LineCommandServerContextFactory final
    : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override {
        return new LineCommandServerContext(socketConnection);
    }
};

#endif
