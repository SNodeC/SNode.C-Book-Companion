#ifndef MINIGATEWAY_SOCKET_STATE_REPORTER_H
#define MINIGATEWAY_SOCKET_STATE_REPORTER_H

#include <core/socket/SocketAddress.h>
#include <core/socket/State.h>
#include <string>

namespace minigateway {

    void reportState(const std::string& instanceName,
                     const core::socket::SocketAddress& socketAddress,
                     const core::socket::State& state);

} // namespace minigateway

#endif // MINIGATEWAY_SOCKET_STATE_REPORTER_H
