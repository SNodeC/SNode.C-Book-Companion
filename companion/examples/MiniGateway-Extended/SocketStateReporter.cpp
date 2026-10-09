#include "SocketStateReporter.h"

#include <Log.h>

namespace minigateway {

    void reportState(const std::string& instanceName,
                     const core::socket::SocketAddress& socketAddress,
                     const core::socket::State& state) {
        switch (state) {
            case core::socket::State::OK:
                snode::log::application().trace()
                    << instanceName << ": connected/listening on '"
                    << socketAddress.toString() << "'";
                break;
            case core::socket::State::DISABLED:
                snode::log::application().trace() << instanceName << ": disabled";
                break;
            case core::socket::State::ERROR:
                snode::log::application().error()
                    << instanceName << " " << socketAddress.toString() << ": "
                    << state.what();
                break;
            case core::socket::State::FATAL:
                snode::log::application().critical()
                    << instanceName << " " << socketAddress.toString() << ": "
                    << state.what();
                break;
        }
    }

} // namespace minigateway
