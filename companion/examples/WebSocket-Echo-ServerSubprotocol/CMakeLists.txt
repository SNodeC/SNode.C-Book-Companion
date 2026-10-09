cmake_minimum_required(VERSION 3.14)

project(WebSocketEchoServerSubprotocol LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS websocket-server)

add_library(
    websocket-echo-server-subprotocol SHARED EchoServer.cpp
                                             EchoServerFactory.cpp
)

set_target_properties(
    websocket-echo-server-subprotocol
    PROPERTIES OUTPUT_NAME snodec-websocket-echo-server SOVERSION
                                                        ${SNODEC_SOVERSION}
)

target_link_libraries(
    websocket-echo-server-subprotocol PRIVATE snodec::websocket-server
)

install(
    TARGETS websocket-echo-server-subprotocol
    COMPONENT WebSocketEchoServerSubprotocol
    LIBRARY
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(
    FILES EchoServer.h EchoServerFactory.h
    COMPONENT WebSocketEchoServerSubprotocol
    DESTINATION
        ${CMAKE_INSTALL_INCLUDEDIR}/snodec-book/examples/WebSocket-Echo-ServerSubprotocol
)

add_custom_target(
    deploy-websocket-echo-server-subprotocol
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            WebSocketEchoServerSubprotocol
    DEPENDS websocket-echo-server-subprotocol
    COMMENT "Installing websocket-echo-server-subprotocol"
    VERBATIM
)
