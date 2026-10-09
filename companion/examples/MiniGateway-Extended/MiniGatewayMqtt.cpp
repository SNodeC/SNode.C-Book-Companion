#include "MiniGatewayMqtt.h"

#include "MeasurementJsonCodec.h"

#include <Log.h>
#include <algorithm>
#include <exception>
#include <iot/mqtt/Topic.h>
#include <list>
#include <utility>
#include <utils/system/signal.h>

namespace minigateway {

    std::vector<MiniGatewayMqtt*> MiniGatewayMqtt::clients;

    MiniGatewayMqtt::MiniGatewayMqtt(const std::string& connectionName,
                                     MeasurementModel& measurementModel,
                                     const std::string& clientId,
                                     std::uint16_t keepAlive,
                                     std::string measurementInputTopic,
                                     std::string measurementOutputTopic,
                                     std::uint8_t qoS,
                                     bool retain)
        : iot::mqtt::client::Mqtt(connectionName, clientId, keepAlive, "")
        , measurementModel(measurementModel)
        , measurementInputTopic(std::move(measurementInputTopic))
        , measurementOutputTopic(std::move(measurementOutputTopic))
        , qoS(qoS)
        , retain(retain) {
        clients.push_back(this);
    }

    MiniGatewayMqtt::~MiniGatewayMqtt() {
        clients.erase(std::remove(clients.begin(), clients.end(), this), clients.end());
    }

    void MiniGatewayMqtt::onConnected() {
        snode::log::application().trace() << "MQTT: initiating session";

        sendConnect(true, "", "", 0, false, "", "", false);
    }

    void MiniGatewayMqtt::onDisconnected() {
        connected = false;

        Super::onDisconnected();
    }

    bool MiniGatewayMqtt::onSignal(int signum) {
        snode::log::application().trace()
            << "MQTT: exit due to signal " << signum << " (SIG"
            << utils::system::sigabbrev_np(signum) << ")";

        sendDisconnect();

        return Super::onSignal(signum);
    }

    void MiniGatewayMqtt::onConnack(const iot::mqtt::packets::Connack& connack) {
        if (connack.getReturnCode() == 0) {
            connected = true;

            sendSubscribe(std::list<iot::mqtt::Topic>{
                iot::mqtt::Topic(measurementInputTopic, qoS)});
        } else {
            connected = false;
            sendDisconnect();
        }
    }

    void MiniGatewayMqtt::onPublish(const iot::mqtt::packets::Publish& publish) {
        if (publish.getTopic() != measurementInputTopic) {
            snode::log::application().trace()
                << "Ignoring MQTT publish on unsubscribed topic " << publish.getTopic();
            return;
        }

        snode::log::application().trace()
            << "MQTT measurement input on " << publish.getTopic() << ": "
            << publish.getMessage();

        try {
            measurementModel.accept(fromJsonPayload(publish.getMessage()));
        } catch (const std::exception& ex) {
            snode::log::application().warn()
                << "Ignoring invalid MQTT measurement payload on " << publish.getTopic()
                << ": " << ex.what();
        }
    }

    void MiniGatewayMqtt::publishMeasurement(const Measurement& measurement) const {
        if (connected) {
            sendPublish(measurementOutputTopic, toJsonPayload(measurement), qoS, retain);
        }
    }

    void MiniGatewayMqtt::publishMeasurementToConnected(const Measurement& measurement) {
        const std::vector<MiniGatewayMqtt*> currentClients = clients;

        for (MiniGatewayMqtt* client : currentClients) {
            if (client != nullptr) {
                client->publishMeasurement(measurement);
            }
        }
    }

} // namespace minigateway
