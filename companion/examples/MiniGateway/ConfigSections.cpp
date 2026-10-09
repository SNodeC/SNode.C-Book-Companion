#include "ConfigSections.h"

namespace minigateway {

    ConfigMqtt::ConfigMqtt(utils::SubCommand* parent)
        : utils::SubCommand(parent, this, "MiniGateway")
        , clientIdOpt(setConfigurable(addOption("--client-id",
                                                "MQTT Client-ID",
                                                "string",
                                                "minigateway",
                                                CLI::TypeValidator<std::string>()),
                                      true))
        , keepAliveOpt(setConfigurable(addOption("--keep-alive",
                                                 "MQTT keep-alive in seconds",
                                                 "uint16_t",
                                                 "30",
                                                 CLI::TypeValidator<std::uint16_t>()),
                                       true))
        , measurementInputTopicOpt(
              setConfigurable(addOption("--measurement-input-topic",
                                        "MQTT measurement input topic",
                                        "string",
                                        "minigateway/measurement/input",
                                        CLI::TypeValidator<std::string>()),
                              true))
        , measurementOutputTopicOpt(
              setConfigurable(addOption("--measurement-output-topic",
                                        "MQTT measurement output topic",
                                        "string",
                                        "minigateway/measurement/output",
                                        CLI::TypeValidator<std::string>()),
                              true))
        , qoSOpt(setConfigurable(
              addOption("--qos",
                        "MQTT QoS for MiniGateway input and output topics",
                        "uint8_t",
                        "0",
                        CLI::Range(0, 2)),
              true))
        , retainOpt(setConfigurable(addFlag("--retain{true}",
                                            "Retain outgoing measurement publications",
                                            "bool",
                                            "false",
                                            CLI::IsMember({"true", "false"})),
                                    true)) {
    }

    ConfigMqtt::~ConfigMqtt() = default;

    std::string ConfigMqtt::getClientId() const {
        return clientIdOpt->as<std::string>();
    }

    std::uint16_t ConfigMqtt::getKeepAlive() const {
        return keepAliveOpt->as<std::uint16_t>();
    }

    std::string ConfigMqtt::getMeasurementInputTopic() const {
        return measurementInputTopicOpt->as<std::string>();
    }

    std::string ConfigMqtt::getMeasurementOutputTopic() const {
        return measurementOutputTopicOpt->as<std::string>();
    }

    std::uint8_t ConfigMqtt::getQoS() const {
        return qoSOpt->as<std::uint8_t>();
    }

    bool ConfigMqtt::getRetain() const {
        return retainOpt->as<bool>();
    }

} // namespace minigateway
