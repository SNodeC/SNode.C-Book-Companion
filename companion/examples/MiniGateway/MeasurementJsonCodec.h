#ifndef MINIGATEWAY_MEASUREMENT_JSON_CODEC_H
#define MINIGATEWAY_MEASUREMENT_JSON_CODEC_H

#include "Measurement.h"

#include <nlohmann/json.hpp>
#include <string>

namespace minigateway {

    nlohmann::json toJson(const Measurement& measurement);
    std::string toJsonPayload(const Measurement& measurement);
    Measurement fromJson(const nlohmann::json& json);
    Measurement fromJsonPayload(const std::string& payload);

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_JSON_CODEC_H
