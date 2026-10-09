#pragma once

#include "MeasurementModel.h"

#include <core/socket/stream/SocketContextFactory.h>
#include <functional>

namespace minigateway {

    class MiniGatewayMqttSocketContextFactory
        : public core::socket::stream::SocketContextFactory {
    public:
        explicit MiniGatewayMqttSocketContextFactory(
            std::reference_wrapper<MeasurementModel> measurementModel);

    private:
        core::socket::stream::SocketContext*
        create(core::socket::stream::SocketConnection* socketConnection) final;

        MeasurementModel& measurementModel;
    };

} // namespace minigateway
