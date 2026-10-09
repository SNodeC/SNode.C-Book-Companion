#include "MiniGatewayMqttSocketContextFactory.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"

#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <net/config/ConfigInstance.h>

namespace minigateway {

    MiniGatewayMqttSocketContextFactory::MiniGatewayMqttSocketContextFactory(
        std::reference_wrapper<MeasurementModel> measurementModel)
        : measurementModel(measurementModel.get()) {
    }

    core::socket::stream::SocketContext* MiniGatewayMqttSocketContextFactory::create(
        core::socket::stream::SocketConnection* socketConnection) {
        const ConfigMqtt* configMqtt =
            socketConnection->getConfigInstance()->getSubCommand<ConfigMqtt>();

        return new iot::mqtt::SocketContext(
            socketConnection,
            new MiniGatewayMqtt(socketConnection->getConnectionName(),
                                measurementModel,
                                configMqtt->getClientId(),
                                configMqtt->getKeepAlive(),
                                configMqtt->getMeasurementInputTopic(),
                                configMqtt->getMeasurementOutputTopic(),
                                configMqtt->getQoS(),
                                configMqtt->getRetain()));
    }

} // namespace minigateway
