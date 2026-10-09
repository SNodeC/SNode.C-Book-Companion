#ifndef MINIGATEWAY_MQTT_CLIENT_H
#define MINIGATEWAY_MQTT_CLIENT_H

#include "MeasurementModel.h"
#include "MiniGatewayMqttSocketContextFactory.h"

#include <functional>
#include <net/in/stream/legacy/SocketClient.h>

namespace minigateway {

    using MiniGatewayMqttClient =
        net::in::stream::legacy::SocketClient<MiniGatewayMqttSocketContextFactory,
                                              std::reference_wrapper<MeasurementModel>>;

    MiniGatewayMqttClient startMqttIntegrationRole(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_MQTT_CLIENT_H
