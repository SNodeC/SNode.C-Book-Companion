#include "LineCommandServerContextFactory.h"

#include <Log.h>
#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <net/in/stream/legacy/SocketServer.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using LineProtocolServer =
        net::in::stream::legacy::SocketServer<LineCommandServerContextFactory>;

    LineProtocolServer server("lineprotocolserver");

    server.listen(8090,
                  5,
                  [instanceName = server.getConfig()->getInstanceName()](
                      const LineProtocolServer::SocketAddress& socketAddress,
                      const core::socket::State& state) {
                      switch (state) {
                          case core::socket::State::OK:
                              snode::log::application().trace()
                                  << instanceName << ": listening on '"
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
