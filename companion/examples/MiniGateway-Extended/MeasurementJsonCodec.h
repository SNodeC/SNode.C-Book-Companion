#pragma once

#include "Measurement.h"

#include <nlohmann/json.hpp>
#include <string>

namespace minigateway {

    nlohmann::json toJson(const Measurement& measurement);
    std::string toJsonPayload(const Measurement& measurement);
    Measurement fromJson(const nlohmann::json& json);
    Measurement fromJsonPayload(const std::string& payload);

} // namespace minigateway
