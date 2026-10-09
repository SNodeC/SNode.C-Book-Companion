#include "MeasurementJsonCodec.h"
#include "MeasurementModel.h"

#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

int main() {
    minigateway::MeasurementModel model;
    unsigned notifications = 0;
    const auto subscription = model.subscribe([&](const auto&) {
        ++notifications;
    });
    const std::string valid =
        R"({"temperature":21.5,"humidity":43,"voltage":3.72,"sequence":900})";
    model.accept(minigateway::fromJsonPayload(valid));
    const auto before = minigateway::toJson(model.current());
    for (const auto& payload :
         {std::string("{"), std::string(R"({"temperature":21.5})")}) {
        bool rejected = false;
        try {
            model.accept(minigateway::fromJsonPayload(payload));
        } catch (const nlohmann::json::exception&) {
            rejected = true;
        }
        if (!rejected || minigateway::toJson(model.current()) != before ||
            notifications != 1) {
            throw std::runtime_error("invalid payload reached acceptance");
        }
    }
    auto nonfinite = nlohmann::json::parse(valid);
    nonfinite["temperature"] = std::numeric_limits<double>::infinity();
    bool rejected = false;
    try {
        model.accept(minigateway::fromJson(nonfinite));
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    if (!rejected || minigateway::toJson(model.current()) != before ||
        notifications != 1) {
        throw std::runtime_error("non-finite value reached acceptance");
    }
    const auto accepted = model.accept(minigateway::fromJsonPayload(valid));
    model.unsubscribe(subscription);
    if (accepted.sequence != 2 || notifications != 2) {
        throw std::runtime_error("rejected input consumed an acceptance sequence");
    }
    std::cout << "PASS: three invalid inputs leave state and notifications unchanged; "
                 "next acceptance is 2\n";
}
