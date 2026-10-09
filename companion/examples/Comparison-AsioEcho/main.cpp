#include <array>
#include <asio.hpp>
#include <charconv>
#include <csignal>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string_view>
#include <utility>

using asio::ip::tcp;

class Session : public std::enable_shared_from_this<Session> {
public:
    explicit Session(tcp::socket socket)
        : socket(std::move(socket)) {
    }

    void read() {
        socket.async_read_some(
            asio::buffer(bytes),
            [self = shared_from_this()](std::error_code error, std::size_t size) {
                if (!error) {
                    self->write(size);
                }
            });
    }

private:
    void write(std::size_t size) {
        asio::async_write(
            socket,
            asio::buffer(bytes.data(), size),
            [self = shared_from_this()](std::error_code error, std::size_t) {
                if (!error) {
                    self->read();
                }
            });
    }

    tcp::socket socket;
    std::array<char, 4096> bytes{};
};

class Server {
public:
    Server(asio::io_context& loop, unsigned short port)
        : acceptor(loop, tcp::endpoint(asio::ip::make_address("127.0.0.1"), port)) {
        accept();
    }

private:
    void accept() {
        acceptor.async_accept([this](std::error_code error, tcp::socket socket) {
            if (error) {
                throw std::system_error(error);
            }
            std::make_shared<Session>(std::move(socket))->read();
            accept();
        });
    }

    tcp::acceptor acceptor;
};

int main(int argc, char* argv[]) {
    try {
        unsigned int port = 8081;
        if (argc > 2) {
            throw std::invalid_argument("usage: asio-echo [port]");
        }
        if (argc == 2) {
            const std::string_view value(argv[1]);
            const auto result =
                std::from_chars(value.data(), value.data() + value.size(), port);
            if (result.ec != std::errc{} || result.ptr != value.data() + value.size() ||
                port == 0 || port > 65535) {
                throw std::invalid_argument("port must be an integer from 1 to 65535");
            }
        }
        asio::io_context loop;
        Server server(loop, static_cast<unsigned short>(port));
        asio::signal_set signals(loop, SIGINT, SIGTERM);
        signals.async_wait([&loop](std::error_code, int) {
            loop.stop();
        });
        loop.run();
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
