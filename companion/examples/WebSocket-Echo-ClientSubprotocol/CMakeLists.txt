cmake_minimum_required(VERSION 3.14)

project(WebSocketEchoClientSubprotocol LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS websocket-client)

add_library(
    websocket-echo-client-subprotocol SHARED EchoClient.cpp
                                             EchoClientFactory.cpp
)

set_target_properties(
    websocket-echo-client-subprotocol
    PROPERTIES OUTPUT_NAME snodec-websocket-echo-client SOVERSION
                                                        ${SNODEC_SOVERSION}
)

target_link_libraries(
    websocket-echo-client-subprotocol PRIVATE snodec::websocket-client
)

install(
    TARGETS websocket-echo-client-subprotocol
    COMPONENT WebSocketEchoClientSubprotocol
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(
    FILES EchoClient.h EchoClientFactory.h
    COMPONENT WebSocketEchoClientSubprotocol
    DESTINATION
        ${CMAKE_INSTALL_INCLUDEDIR}/snodec-book/examples/WebSocket-Echo-ClientSubprotocol
)

add_custom_target(
    deploy-websocket-echo-client-subprotocol
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            WebSocketEchoClientSubprotocol
    DEPENDS websocket-echo-client-subprotocol
    COMMENT "Installing websocket-echo-client-subprotocol"
    VERBATIM
)
