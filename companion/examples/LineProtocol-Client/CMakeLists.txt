cmake_minimum_required(VERSION 3.14)

project(LineProtocolClient LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS net-in-stream-legacy)

add_executable(
    line-protocol-client
    main.cpp LineCommandClientContext.cpp LineCommandClientContext.h
    LineCommandClientContextFactory.h
)

target_link_libraries(line-protocol-client PRIVATE snodec::net-in-stream-legacy)

install(
    TARGETS line-protocol-client
    COMPONENT LineProtocolClient
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-line-protocol-client
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            LineProtocolClient
    DEPENDS line-protocol-client
    COMMENT "Installing line-protocol-client"
    VERBATIM
)
