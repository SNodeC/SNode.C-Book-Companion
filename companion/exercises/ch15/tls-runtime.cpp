#include <core/SNodeC.h>
#include <core/socket/stream/SocketContext.h>
#include <core/socket/stream/SocketContextFactory.h>
#include <iostream>
#include <net/in/stream/tls/SocketClient.h>
#include <openssl/ssl.h>
#include <openssl/x509v3.h>
class Context : public core::socket::stream::SocketContext {
public:
    explicit Context(core::socket::stream::SocketConnection* connection)
        : SocketContext(connection) {
    }

private:
    void onConnected() override {
    }
    void onDisconnected() override {
    }
    bool onSignal(int) override {
        return true;
    }
    std::size_t onReceivedFromPeer() override {
        char buffer[64];
        return readFromPeer(buffer, sizeof(buffer));
    }
};
class Factory : public core::socket::stream::SocketContextFactory {
public:
    Factory() = default;
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* c) override {
        return new Context(c);
    }
};
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);
    using Client = net::in::stream::tls::SocketClient<Factory>;
    Client client("probe");
    bool earlyNull = false, ready = false;
    client.setOnConnect([&](auto* connection) {
        earlyNull = connection->getSSL() == nullptr;
        X509_VERIFY_PARAM* parameters =
            SSL_CTX_get0_param(connection->getConfig()->getSslCtx());
        X509_VERIFY_PARAM_set_hostflags(parameters, X509_CHECK_FLAG_NO_PARTIAL_WILDCARDS);
        if (X509_VERIFY_PARAM_set1_host(parameters, "sensor.example", 0) != 1)
            connection->close();
    });
    client.setOnConnected([&](auto*) {
        ready = true;
        core::SNodeC::stop();
    });
    client.setOnDisconnect([](auto*) {
        core::SNodeC::stop();
    });
    client.connect([](const auto&, auto) {
    });
    const auto result = core::SNodeC::start();
    std::cout << "early_ssl_null=" << earlyNull << " ready=" << ready
              << " result=" << result << '\n';
    return earlyNull && result == 0 ? 0 : 1;
}
