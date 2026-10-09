#include "MeasurementModel.h"

#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    minigateway::MeasurementModel model;
    std::vector<std::uint64_t> first, second;
    const auto a = model.subscribe([&](const auto& value) {
        first.push_back(value.sequence);
    });
    const auto b = model.subscribe([&](const auto& value) {
        second.push_back(value.sequence);
    });
    minigateway::Measurement input;
    for (auto supplied : {900U, 2U}) {
        input.sequence = supplied;
        model.accept(input);
    }
    model.unsubscribe(a);
    input.sequence = 1;
    const auto accepted = model.accept(input);
    model.unsubscribe(b);
    if (first != std::vector<std::uint64_t>{1, 2} ||
        second != std::vector<std::uint64_t>{1, 2, 3} || accepted.sequence != 3 ||
        model.current().sequence != 3) {
        throw std::runtime_error("acceptance order or observer lifetime differs");
    }
    std::cout
        << "PASS: input 900,2,1 -> accepted 1,2,3; detached observer sees only 1,2\n";
}
