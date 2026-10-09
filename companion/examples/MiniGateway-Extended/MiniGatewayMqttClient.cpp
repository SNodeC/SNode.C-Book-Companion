#include "MiniGatewayMqttClient.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"
#include "SocketStateReporter.h"

#include <net/config/ConfigInstance.h>

namespace minigateway {

    namespace {

        void
        createMqttConfig(net::in::stream::legacy::config::ConfigSocketClient& config) {
            config.Instance::newSubCommand<ConfigMqtt>();
        }

    } // namespace

    MiniGatewayMqttClient startMqttIntegrationRole(MeasurementModel& measurementModel) {
        MiniGatewayMqttClient socketClient("mqtt-uplink", std::ref(measurementModel));

        auto* config = socketClient.getConfig();
        config->Remote::setPort(1883);
        config->setDisableNagleAlgorithm();
        createMqttConfig(*config);

        socketClient.getConfig()->setRetry();
        socketClient.getConfig()->setRetryBase(1);
        socketClient.getConfig()->setReconnect();

        measurementModel.subscribe([](const Measurement& measurement) {
            MiniGatewayMqtt::publishMeasurementToConnected(measurement);
        });

        socketClient.connect([](const MiniGatewayMqttClient::SocketAddress& socketAddress,
                                const core::socket::State& state) {
            reportState("mqtt-uplink", socketAddress, state);
        });

        return socketClient;
    }

} // namespace minigateway
