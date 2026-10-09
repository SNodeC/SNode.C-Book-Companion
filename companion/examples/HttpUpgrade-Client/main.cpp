#include <Log.h>
#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <memory>
#include <string>
#include <web/http/legacy/in/Client.h>
#include <web/websocket/client/SocketContextUpgradeFactory.h>

using Client = web::http::legacy::in::Client;
using MasterRequest = Client::MasterRequest;
using Request = Client::Request;
using Response = Client::Response;
using SocketAddress = Client::SocketAddress;

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    web::websocket::client::SocketContextUpgradeFactory::link();

    const Client client(
        "legacy",
        [](const std::shared_ptr<MasterRequest>& req) {
            req->set("Sec-WebSocket-Protocol", "subprotocol, echo");

            req->upgrade(
                "/ws",
                "websocket",
                [](bool success) {
                    snode::log::application().trace()
                        << "upgrade request initiation: "
                        << (success ? "accepted" : "rejected");
                },
                [](const std::shared_ptr<Request>&,
                   const std::shared_ptr<Response>&,
                   bool success) {
                    snode::log::application().trace()
                        << "upgrade response: " << (success ? "accepted" : "rejected");
                },
                [](const std::shared_ptr<Request>&, const std::string& message) {
                    snode::log::application().error()
                        << "upgrade response parse error: " << message;
                });
        },
        [](const std::shared_ptr<MasterRequest>&) {
            snode::log::application().trace() << "HTTP request completed or disconnected";
        });

    client.connect([](const SocketAddress& socketAddress, const core::socket::State&) {
        snode::log::application().trace()
            << "HTTP client connection status for " << socketAddress.toString();
    });

    return core::SNodeC::start();
}
