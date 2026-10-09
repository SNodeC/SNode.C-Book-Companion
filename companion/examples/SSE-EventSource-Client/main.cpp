#include <Log.h>
#include <core/SNodeC.h>
#include <net/in/SocketAddress.h>
#include <web/http/legacy/in/EventSource.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const net::in::SocketAddress address{"127.0.0.1", 8080};

    auto events = web::http::legacy::in::EventSource("http", address, "/events");

    events->onOpen([] {
        snode::log::application().trace() << "SSE stream opened";
    });

    events->onMessage(
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            snode::log::application().trace() << "message: " << event.data;
        });

    events->addEventListener(
        "measurement",
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            snode::log::application().trace() << "measurement: " << event.data;
        });

    events->onError([] {
        snode::log::application().error() << "SSE stream error";
    });

    return core::SNodeC::start();
}
