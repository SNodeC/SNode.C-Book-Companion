#include "MeasurementUnixSocketServer.h"

#include "SocketStateReporter.h"

namespace minigateway {

    MeasurementSocketServer
    startMeasurementInputRole(MeasurementModel& measurementModel) {
        MeasurementSocketServer socketServer("measurement-input",
                                             std::ref(measurementModel));

        socketServer.listen(
            "/tmp/minigateway-measurements.sock",
            [](const MeasurementSocketServer::SocketAddress& socketAddress,
               const core::socket::State& state) {
                reportState("measurement-input", socketAddress, state);
            });

        return socketServer;
    }

} // namespace minigateway
