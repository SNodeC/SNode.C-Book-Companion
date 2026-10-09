#include "EchoSocketContext.h"

#include <Log.h>
#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <net/in/stream/legacy/SocketServer.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoServer =
        net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>;

    EchoServer server("echoserver");

    server.listen(8080,
                  5,
                  [instanceName = server.getConfig()->getInstanceName()](
                      const EchoServer::SocketAddress& socketAddress,
                      const core::socket::State& state) {
                      switch (state) {
                          case core::socket::State::OK:
                              snode::log::application("echo").info()
                                  << instanceName << ": listening on '"
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
