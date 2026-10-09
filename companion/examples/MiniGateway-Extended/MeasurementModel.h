#pragma once

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementModel {
    public:
        using Listener = std::function<void(const Measurement&)>;

        using Subscription = std::list<Listener>::iterator;

        Measurement current() const;
        Measurement accept(Measurement measurement);
        Subscription subscribe(Listener listener);
        void unsubscribe(Subscription subscription);

    private:
        void publish(const Measurement& measurement);

        Measurement currentMeasurement;
        std::list<Listener> listeners;
    };

} // namespace minigateway
