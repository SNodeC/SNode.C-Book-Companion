cmake_minimum_required(VERSION 3.14)

project(SSEEventSourceClient LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS http-client net-in-stream-legacy)

add_executable(sse-eventsource-client main.cpp)

target_link_libraries(
    sse-eventsource-client PRIVATE snodec::http-client
                                   snodec::net-in-stream-legacy
)

install(
    TARGETS sse-eventsource-client
    COMPONENT SSEEventSourceClient
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-sse-eventsource-client
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            SSEEventSourceClient
    DEPENDS sse-eventsource-client
    COMMENT "Installing sse-eventsource-client"
    VERBATIM
)
