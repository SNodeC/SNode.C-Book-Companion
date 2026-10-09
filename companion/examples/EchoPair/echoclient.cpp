#include "EchoSocketContext.h"

#include <Log.h>
#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <net/in/stream/legacy/SocketClient.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoClient =
        net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>;

    EchoClient client("echoclient");

    client.connect("localhost",
                   8080,
                   [instanceName = client.getConfig()->getInstanceName()](
                       const EchoClient::SocketAddress& socketAddress,
                       const core::socket::State& state) {
                       switch (state) {
                           case core::socket::State::OK:
                               snode::log::application("echo").info()
                                   << instanceName << ": connected to '"
                                   << socketAddress.toString() << "'";
                               break;
                           case core::socket::State::DISABLED:
                               snode::log::application("echo").info()
                                   << instanceName << ": disabled";
                               break;
                           case core::socket::State::ERROR:
                               snode::log::application("echo").error()
                                   << instanceName << ": " << socketAddress.toString()
                                   << ": " << state.what();
                               break;
                           case core::socket::State::FATAL:
                               snode::log::application("echo").critical()
                                   << instanceName << ": " << socketAddress.toString()
                                   << ": " << state.what();
                               break;
                       }
                   });

    return core::SNodeC::start();
}
