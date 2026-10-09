cmake_minimum_required(VERSION 3.14)

project(MQTTClientRole LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS mqtt-client)

add_library(mqtt-client-role SensorClient.cpp SensorClient.h)

target_link_libraries(mqtt-client-role PRIVATE snodec::mqtt-client)

install(
    TARGETS mqtt-client-role
    COMPONENT MQTTClientRole
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(
    FILES SensorClient.h
    COMPONENT MQTTClientRole
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/snodec-book/examples/MQTT-ClientRole
)

add_custom_target(
    deploy-mqtt-client-role
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            MQTTClientRole
    DEPENDS mqtt-client-role
    COMMENT "Installing mqtt-client-role"
    VERBATIM
)
