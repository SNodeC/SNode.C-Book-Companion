#include "MiniGatewayWeb.h"

#include "MeasurementJsonCodec.h"
#include "SocketStateReporter.h"

#include <chrono>
#include <cstdint>
#include <express/middleware/VerboseRequest.h>
#include <memory>
#include <string>
#include <web/http/http_utils.h>
#include <web/http/server/SocketContext.h>

namespace minigateway {

    namespace {

        using Request = MiniGatewayWebApp::Request;
        using Response = MiniGatewayWebApp::Response;

        Measurement makeSimulatedMeasurement(std::uint64_t sampleIndex) {
            Measurement measurement;
            measurement.temperature = 20.0 + static_cast<double>(sampleIndex % 50) / 10.0;
            measurement.humidity = 40.0 + static_cast<double>(sampleIndex % 20);
            measurement.voltage = 3.7 + static_cast<double>(sampleIndex % 10) / 100.0;
            measurement.timestamp = std::chrono::system_clock::now();

            return measurement;
        }

        static bool acceptsEventStream(const std::shared_ptr<Request>& req) {
            return web::http::ciEquals(req->get("Accept"), "text/event-stream");
        }

        static void sendMeasurement(const std::shared_ptr<Response>& res,
                                    const Measurement& measurement) {
            res->sendFragment("event: measurement");
            res->sendFragment("id: " + std::to_string(measurement.sequence));
            res->sendFragment("data: " + toJsonPayload(measurement));
            res->sendFragment("");
        }

        void registerWebRoutes(const MiniGatewayWebApp& app,
                               MeasurementModel& measurementModel) {
            app.use(express::middleware::VerboseRequest());

            app.get("/health", [] APPLICATION(req, res) {
                res->json({{"ok", true}});
            });

            app.get("/status", [&measurementModel] APPLICATION(req, res) {
                res->json(toJson(measurementModel.current()));
            });

            app.get("/events", [&measurementModel] APPLICATION(req, res) {
                if (acceptsEventStream(req)) {
                    res->set("Content-Type", "text/event-stream")
                        .set("Cache-Control", "no-cache")
                        .set("Connection", "keep-alive");
                    res->sendHeader();

                    const Measurement current = measurementModel.current();
                    if (current.sequence > 0) {
                        sendMeasurement(res, current);
                    }

                    const auto subscription =
                        measurementModel.subscribe([res](const Measurement& measurement) {
                            sendMeasurement(res, measurement);
                        });
                    res->getSocketContext()->setOnDisconnected(
                        [&measurementModel, subscription] {
                            measurementModel.unsubscribe(subscription);
                        });
                } else {
                    res->status(406).send("SSE requires Accept: text/event-stream");
                }
            });

            app.post("/simulate", [&measurementModel] APPLICATION(req, res) {
                const Measurement measurement =
                    makeSimulatedMeasurement(measurementModel.current().sequence + 1);
                const Measurement acceptedMeasurement =
                    measurementModel.accept(measurement);

                res->json(toJson(acceptedMeasurement));
            });
        }

    } // namespace

    MiniGatewayWebApp startWebRole(MeasurementModel& measurementModel) {
        MiniGatewayWebApp app("web");

        registerWebRoutes(app, measurementModel);

        app.listen(8080,
                   [instanceName = app.getConfig()->getInstanceName()](
                       const MiniGatewayWebApp::SocketAddress& socketAddress,
                       const core::socket::State& listenState) {
                       reportState(instanceName, socketAddress, listenState);
                   });

        return app;
    }

} // namespace minigateway
