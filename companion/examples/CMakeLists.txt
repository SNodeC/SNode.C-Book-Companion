cmake_minimum_required(VERSION 3.14)

project(SNodeCBookExamples LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

set(SNODEC_BOOK_EXAMPLE_DIRS
    EchoPair
    Comparison-AsioEcho
    SemanticLogging
    HttpUpgrade-Server
    HttpUpgrade-Client
    SSE-Server
    SSE-EventSource-Client
    WebSocket-Echo-ServerSubprotocol
    WebSocket-Echo-ClientSubprotocol
    LineProtocol-Server
    LineProtocol-Client
    MQTT-ClientRole
    MariaDB-Minimal
    MiniGateway
    MiniGateway-Extended
)

foreach(EXAMPLE_DIR IN LISTS SNODEC_BOOK_EXAMPLE_DIRS)
    add_subdirectory("${EXAMPLE_DIR}")
endforeach()

set(SNODEC_BOOK_EXAMPLE_TARGETS
    echoserver
    asio-echo
    echoclient
    semantic-logging
    http-upgrade-server
    http-upgrade-client
    sse-server
    sse-eventsource-client
    websocket-echo-server-subprotocol
    websocket-echo-client-subprotocol
    line-protocol-server
    line-protocol-client
    mqtt-client-role
    mariadb-minimal
    minigateway
    minigateway-extended
)

add_custom_target(all-examples DEPENDS ${SNODEC_BOOK_EXAMPLE_TARGETS})

add_custom_target(
    deploy-examples
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}"
    DEPENDS ${SNODEC_BOOK_EXAMPLE_TARGETS}
    COMMENT "Installing all SNode.C book examples"
    VERBATIM
)
