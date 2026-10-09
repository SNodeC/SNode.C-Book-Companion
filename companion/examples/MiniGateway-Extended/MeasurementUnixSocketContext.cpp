#include "MeasurementUnixSocketContext.h"

#include <Log.h>
#include <algorithm>
#include <cctype>
#include <chrono>
#include <cmath>
#include <core/socket/SocketAddress.h>
#include <core/socket/stream/SocketConnection.h>
#include <exception>
#include <stdexcept>
#include <utility>
#include <vector>

namespace minigateway {

    namespace {

        std::string trim(std::string value) {
            value.erase(value.begin(),
                        std::find_if(value.begin(), value.end(), [](unsigned char ch) {
                            return !std::isspace(ch);
                        }));
            value.erase(std::find_if(value.rbegin(),
                                     value.rend(),
                                     [](unsigned char ch) {
                                         return !std::isspace(ch);
                                     })
                            .base(),
                        value.end());

            return value;
        }

        std::vector<std::string> splitCsvLine(const std::string& line) {
            std::vector<std::string> values;
            std::size_t valueStart = 0;

            while (valueStart <= line.length()) {
                const std::size_t valueEnd = line.find(',', valueStart);
                values.push_back(trim(line.substr(valueStart, valueEnd - valueStart)));

                if (valueEnd == std::string::npos) {
                    break;
                }
                valueStart = valueEnd + 1;
            }

            return values;
        }

        double parseDouble(const std::string& value, const std::string& fieldName) {
            std::size_t parsedLength = 0;
            const double parsedValue = std::stod(value, &parsedLength);
            if (parsedLength != value.length() || !std::isfinite(parsedValue)) {
                throw std::invalid_argument("invalid " + fieldName + " value '" + value +
                                            "'");
            }

            return parsedValue;
        }

        std::uint64_t parseSequence(const std::string& value) {
            std::size_t parsedLength = 0;
            const auto parsedValue = std::stoull(value, &parsedLength);
            if (parsedLength != value.length()) {
                throw std::invalid_argument("invalid sequence value '" + value + "'");
            }

            return parsedValue;
        }

        Measurement parseMeasurementLine(const std::string& line) {
            const std::vector<std::string> values = splitCsvLine(line);
            if (values.size() != 3 && values.size() != 4) {
                throw std::invalid_argument(
                    "expected temperature,humidity,voltage[,sequence]");
            }

            Measurement measurement;
            measurement.temperature = parseDouble(values[0], "temperature");
            measurement.humidity = parseDouble(values[1], "humidity");
            measurement.voltage = parseDouble(values[2], "voltage");
            measurement.sequence = values.size() == 4 ? parseSequence(values[3]) : 0;
            measurement.timestamp = std::chrono::system_clock::now();

            return measurement;
        }

    } // namespace

    MeasurementUnixSocketContext::MeasurementUnixSocketContext(
        core::socket::stream::SocketConnection* socketConnection,
        MeasurementModel& measurementModel)
        : core::socket::stream::SocketContext(socketConnection)
        , measurementModel(measurementModel) {
    }

    void MeasurementUnixSocketContext::onConnected() {
        snode::log::application().trace()
            << "Measurement socket connected from "
            << getSocketConnection()->getRemoteAddress().toString();
    }

    void MeasurementUnixSocketContext::onDisconnected() {
        snode::log::application().trace()
            << "Measurement socket disconnected from "
            << getSocketConnection()->getRemoteAddress().toString();
    }

    bool MeasurementUnixSocketContext::onSignal(int signum) {
        snode::log::application().trace()
            << "Measurement socket disconnected due to signal " << signum;

        return true;
    }

    std::size_t MeasurementUnixSocketContext::onReceivedFromPeer() {
        char chunk[4096];
        const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

        if (chunkLen > 0) {
            receiveBuffer.append(chunk, chunkLen);

            std::size_t lineEnd = receiveBuffer.find('\n');
            while (lineEnd != std::string::npos && lineEnd <= 4096) {
                std::string line = receiveBuffer.substr(0, lineEnd);
                if (!line.empty() && line.back() == '\r') {
                    line.pop_back();
                }

                processLine(line);
                receiveBuffer.erase(0, lineEnd + 1);
                lineEnd = receiveBuffer.find('\n');
            }

            if (receiveBuffer.length() > 4096) {
                snode::log::application().warn()
                    << "Measurement socket line exceeds 4096 bytes; closing connection";
                close();
            }
        }

        return chunkLen;
    }

    void MeasurementUnixSocketContext::processLine(const std::string& line) const {
        if (!line.empty()) {
            try {
                measurementModel.accept(parseMeasurementLine(line));
            } catch (const std::exception& ex) {
                snode::log::application().warn() << "Ignoring invalid measurement line '"
                                                 << line << "': " << ex.what();
            }
        }
    }

} // namespace minigateway
