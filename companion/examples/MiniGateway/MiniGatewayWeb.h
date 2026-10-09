#ifndef MINIGATEWAY_WEB_H
#define MINIGATEWAY_WEB_H

#include "MeasurementModel.h"

#include <express/legacy/in/WebApp.h>

namespace minigateway {

    using MiniGatewayWebApp = express::legacy::in::WebApp;

    MiniGatewayWebApp startWebRole(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_WEB_H
