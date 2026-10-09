#include "MeasurementModel.h"

#include <utility>

namespace minigateway {

    Measurement MeasurementModel::current() const {
        return currentMeasurement;
    }

    Measurement MeasurementModel::accept(Measurement measurement) {
        measurement.sequence = currentMeasurement.sequence + 1;

        currentMeasurement = std::move(measurement);
        publish(currentMeasurement);

        return currentMeasurement;
    }

    MeasurementModel::Subscription MeasurementModel::subscribe(Listener listener) {
        return listeners.insert(listeners.end(), std::move(listener));
    }

    void MeasurementModel::unsubscribe(Subscription subscription) {
        listeners.erase(subscription);
    }

    void MeasurementModel::publish(const Measurement& measurement) {
        for (const auto& listener : listeners) {
            listener(measurement);
        }
    }

} // namespace minigateway
