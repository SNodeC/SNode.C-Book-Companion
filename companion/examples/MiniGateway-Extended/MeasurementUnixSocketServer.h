#pragma once

#include "MeasurementModel.h"
#include "MeasurementUnixSocketContextFactory.h"

#include <functional>
#include <net/un/stream/legacy/SocketServer.h>

namespace minigateway {

    using MeasurementSocketServer =
        net::un::stream::legacy::SocketServer<MeasurementUnixSocketContextFactory,
                                              std::reference_wrapper<MeasurementModel>>;

    MeasurementSocketServer startMeasurementInputRole(MeasurementModel& measurementModel);

} // namespace minigateway
