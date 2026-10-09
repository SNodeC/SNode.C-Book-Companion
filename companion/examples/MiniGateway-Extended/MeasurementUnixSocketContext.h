#pragma once

#include "MeasurementModel.h"

#include <core/socket/stream/SocketContext.h>
#include <cstdint>
#include <string>

namespace minigateway {

    class MeasurementUnixSocketContext : public core::socket::stream::SocketContext {
    public:
        MeasurementUnixSocketContext(
            core::socket::stream::SocketConnection* socketConnection,
            MeasurementModel& measurementModel);

    private:
        void onConnected() final;
        void onDisconnected() final;
        [[nodiscard]] bool onSignal(int signum) final;
        std::size_t onReceivedFromPeer() final;

        void processLine(const std::string& line) const;

        MeasurementModel& measurementModel;
        std::string receiveBuffer;
    };

} // namespace minigateway
