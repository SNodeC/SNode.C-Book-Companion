#pragma once

#include "MeasurementModel.h"

#include <express/legacy/in/WebApp.h>

namespace minigateway {

    using MiniGatewayWebApp = express::legacy::in::WebApp;

    MiniGatewayWebApp startWebRole(MeasurementModel& measurementModel);

} // namespace minigateway
