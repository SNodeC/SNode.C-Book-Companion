#pragma once

#include <chrono>
#include <cstdint>

namespace minigateway {

    struct Measurement {
        double temperature = 0.0;
        double humidity = 0.0;
        double voltage = 0.0;
        std::uint64_t sequence = 0;
        std::chrono::system_clock::time_point timestamp =
            std::chrono::system_clock::now();
    };

} // namespace minigateway
