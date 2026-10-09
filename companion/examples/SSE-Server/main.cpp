#include <Log.h>
#include <core/socket/State.h>
#include <cstdint>
#include <express/legacy/in/WebApp.h>
#include <functional>
#include <list>
#include <memory>
#include <nlohmann/json.hpp>
#include <string>
#include <utility>
#include <web/http/http_utils.h>
#include <web/http/server/SocketContext.h>

using WebApp = express::legacy::in::WebApp;
using Request = WebApp::Request;
using Response = WebApp::Response;
using SocketAddress = WebApp::SocketAddress;

struct Measurement {
    std::uint64_t sequence = 0;
    std::string sensor;
    double value = 0.0;

    nlohmann::json toJson() const {
        return {
            {"sequence", sequence},
            {"sensor", sensor},
            {"value", value},
        };
    }
};

class MeasurementPublisher {
public:
    using Listener = std::function<void(const Measurement&)>;
    using Subscription = std::list<Listener>::iterator;
    Measurement current() const {
        return last;
    }

    Subscription subscribe(Listener listener) {
        return listeners.insert(listeners.end(), std::move(listener));
    }

    void unsubscribe(Subscription subscription) {
        listeners.erase(subscription);
    }

    Measurement publish(std::string sensor, double value) {
        last = Measurement{last.sequence + 1, std::move(sensor), value};
        for (const auto& listener : listeners) {
            listener(last);
        }
        return last;
    }

private:
    Measurement last{1, "temperature", 23.5};
    std::list<Listener> listeners;
};

static bool acceptsEventStream(const std::shared_ptr<Request>& req) {
    return web::http::ciEquals(req->get("Accept"), "text/event-stream");
}

static void sendMeasurement(const std::shared_ptr<Response>& res,
                            const Measurement& measurement) {
    res->sendFragment("event: measurement");
    res->sendFragment("id: " + std::to_string(measurement.sequence));
    res->sendFragment("data: " + measurement.toJson().dump());
    res->sendFragment("");
}

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);

    MeasurementPublisher measurements;
    const WebApp app("legacy");

    app.get("/events",
            [&measurements](const std::shared_ptr<Request>& req,
                            const std::shared_ptr<Response>& res) {
                if (acceptsEventStream(req)) {
                    res->set("Content-Type", "text/event-stream")
                        .set("Cache-Control", "no-cache")
                        .set("Connection", "keep-alive")
                        .sendHeader();

                    if (const Measurement current = measurements.current();
                        current.sequence > 0) {
                        sendMeasurement(res, current);
                    }

                    const auto subscription =
                        measurements.subscribe([res](const Measurement& measurement) {
                            sendMeasurement(res, measurement);
                        });
                    res->getSocketContext()->setOnDisconnected(
                        [&measurements, subscription] {
                            measurements.unsubscribe(subscription);
                        });
                } else {
                    res->status(406).send("SSE requires Accept: text/event-stream");
                }
            });

    app.post("/simulate",
             [&measurements](const std::shared_ptr<Request>&,
                             const std::shared_ptr<Response>& res) {
                 const Measurement measurement =
                     measurements.publish("temperature", 24.0);

                 res->set("Content-Type", "application/json")
                     .send(measurement.toJson().dump());
             });

    app.listen([](const SocketAddress& socketAddress, const core::socket::State&) {
        snode::log::application().trace()
            << "SSE server listening on " << socketAddress.toString();
    });

    return express::WebApp::start();
}
