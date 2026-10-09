#include "MeasurementJsonCodec.h"

#include <chrono>
#include <cmath>
#include <stdexcept>

namespace minigateway {

    namespace {

        double readFiniteDouble(const nlohmann::json& json, const char* fieldName) {
            const double value = json.at(fieldName).get<double>();
            if (!std::isfinite(value)) {
                throw std::invalid_argument(std::string("invalid ") + fieldName +
                                            " value");
            }

            return value;
        }

    } // namespace

    nlohmann::json toJson(const Measurement& measurement) {
        return {{"temperature", measurement.temperature},
                {"humidity", measurement.humidity},
                {"voltage", measurement.voltage},
                {"sequence", measurement.sequence}};
    }

    std::string toJsonPayload(const Measurement& measurement) {
        return toJson(measurement).dump();
    }

    Measurement fromJson(const nlohmann::json& json) {
        Measurement measurement;
        measurement.temperature = readFiniteDouble(json, "temperature");
        measurement.humidity = readFiniteDouble(json, "humidity");
        measurement.voltage = readFiniteDouble(json, "voltage");
        measurement.sequence = json.value("sequence", static_cast<std::uint64_t>(0));
        measurement.timestamp = std::chrono::system_clock::now();

        return measurement;
    }

    Measurement fromJsonPayload(const std::string& payload) {
        return fromJson(nlohmann::json::parse(payload));
    }

} // namespace minigateway
