cmake_minimum_required(VERSION 3.14)
project(MiniGatewayExtended LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
include(GNUInstallDirs)
find_package(nlohmann_json 3.7.0 REQUIRED)
find_package(
    snodec 2.0.0 REQUIRED
    COMPONENTS http-server-express-legacy-in net-in-stream-legacy mqtt-client
               net-un-stream-legacy
)
add_executable(
    minigateway-extended
    main.cpp
    MeasurementModel.cpp
    MeasurementJsonCodec.cpp
    MiniGatewayWeb.cpp
    MeasurementUnixSocketServer.cpp
    MeasurementUnixSocketContext.cpp
    MeasurementUnixSocketContextFactory.cpp
    MiniGatewayMqttClient.cpp
    MiniGatewayMqtt.cpp
    MiniGatewayMqttSocketContextFactory.cpp
    SocketStateReporter.cpp
    ConfigSections.cpp
    Measurement.h
    MeasurementModel.h
    MeasurementJsonCodec.h
    MiniGatewayWeb.h
    MeasurementUnixSocketServer.h
    MeasurementUnixSocketContext.h
    MeasurementUnixSocketContextFactory.h
    MiniGatewayMqttClient.h
    MiniGatewayMqtt.h
    MiniGatewayMqttSocketContextFactory.h
    SocketStateReporter.h
    ConfigSections.h
)
target_link_libraries(
    minigateway-extended
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::mqtt-client nlohmann_json::nlohmann_json
            snodec::net-un-stream-legacy
)

install(
    TARGETS minigateway-extended
    COMPONENT MiniGatewayExtended
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-minigateway-extended
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            MiniGatewayExtended
    DEPENDS minigateway-extended
    COMMENT "Installing minigateway-extended"
    VERBATIM
)
