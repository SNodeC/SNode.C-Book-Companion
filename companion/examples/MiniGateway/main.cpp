#include "MeasurementModel.h"
#include "MiniGatewayMqttClient.h"
#include "MiniGatewayWeb.h"

#include <core/SNodeC.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementModel measurementModel;

    const auto webRole = minigateway::startWebRole(measurementModel);
    const auto mqttIntegrationRole =
        minigateway::startMqttIntegrationRole(measurementModel);

    return core::SNodeC::start();
}
