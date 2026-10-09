#pragma once

#include <core/socket/SocketAddress.h>
#include <core/socket/State.h>
#include <string>

namespace minigateway {

    void reportState(const std::string& instanceName,
                     const core::socket::SocketAddress& socketAddress,
                     const core::socket::State& state);

} // namespace minigateway
