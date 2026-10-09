#include "MeasurementUnixSocketContextFactory.h"

#include "MeasurementUnixSocketContext.h"

namespace minigateway {

    MeasurementUnixSocketContextFactory::MeasurementUnixSocketContextFactory(
        std::reference_wrapper<MeasurementModel> measurementModel)
        : measurementModel(measurementModel.get()) {
    }

    core::socket::stream::SocketContext* MeasurementUnixSocketContextFactory::create(
        core::socket::stream::SocketConnection* socketConnection) {
        return new MeasurementUnixSocketContext(socketConnection, measurementModel);
    }

} // namespace minigateway
