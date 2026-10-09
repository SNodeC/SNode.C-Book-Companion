#include "MeasurementModel.h"

#include <iostream>
#include <stdexcept>

int main() {
    minigateway::MeasurementModel shared;
    auto& firstInput = shared;
    auto& secondInput = shared;
    const auto firstShared = firstInput.accept({});
    const auto secondShared = secondInput.accept({});

    minigateway::MeasurementModel firstSeparate, secondSeparate;
    const auto firstOwn = firstSeparate.accept({});
    const auto secondOwn = secondSeparate.accept({});
    if (firstShared.sequence != 1 || secondShared.sequence != 2 ||
        firstOwn.sequence != 1 || secondOwn.sequence != 1 ||
        shared.current().sequence != 2) {
        throw std::runtime_error("model instance ownership differs");
    }
    std::cout
        << "PASS: shared inputs accept 1,2; separate model instances each accept 1\n";
}
