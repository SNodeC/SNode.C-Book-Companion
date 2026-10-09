cmake_minimum_required(VERSION 3.14)

project(SSEServer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)
find_package(snodec 2.0.0 REQUIRED COMPONENTS http-server-express-legacy-in)

add_executable(sse-server main.cpp)

target_link_libraries(
    sse-server PRIVATE snodec::http-server-express-legacy-in
                       nlohmann_json::nlohmann_json
)

install(
    TARGETS sse-server
    COMPONENT SSEServer
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-sse-server
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            SSEServer
    DEPENDS sse-server
    COMMENT "Installing sse-server"
    VERBATIM
)
