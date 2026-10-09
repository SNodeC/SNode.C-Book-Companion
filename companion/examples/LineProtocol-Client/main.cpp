#include "LineCommandClientContextFactory.h"

#include <Log.h>
#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <net/in/stream/legacy/SocketClient.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using LineProtocolClient =
        net::in::stream::legacy::SocketClient<LineCommandClientContextFactory>;

    LineProtocolClient client("lineprotocolclient");

    client.connect("localhost",
                   8090,
                   [instanceName = client.getConfig()->getInstanceName()](
                       const LineProtocolClient::SocketAddress& socketAddress,
                       const core::socket::State& state) {
                       switch (state) {
                           case core::socket::State::OK:
                               snode::log::application().trace()
                                   << instanceName << ": connected to '"
                                   << socketAddress.toString() << "'";
                               break;
                           case core::socket::State::DISABLED:
                               snode::log::application().trace()
                                   << instanceName << ": disabled";
                               break;
                           case core::socket::State::ERROR:
                               snode::log::application().error()
                                   << instanceName << ": " << socketAddress.toString()
                                   << ": " << state.what();
                               break;
                           case core::socket::State::FATAL:
                               snode::log::application().critical()
                                   << instanceName << ": " << socketAddress.toString()
                                   << ": " << state.what();
                               break;
                       }
                   });

    return core::SNodeC::start();
}
