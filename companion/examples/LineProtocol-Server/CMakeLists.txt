cmake_minimum_required(VERSION 3.14)

project(LineProtocolServer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS net-in-stream-legacy)

add_executable(
    line-protocol-server
    main.cpp LineCommandServerContext.cpp LineCommandServerContext.h
    LineCommandServerContextFactory.h
)

target_link_libraries(line-protocol-server PRIVATE snodec::net-in-stream-legacy)

install(
    TARGETS line-protocol-server
    COMPONENT LineProtocolServer
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-line-protocol-server
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            LineProtocolServer
    DEPENDS line-protocol-server
    COMMENT "Installing line-protocol-server"
    VERBATIM
)
