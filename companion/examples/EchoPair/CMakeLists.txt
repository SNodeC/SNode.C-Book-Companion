cmake_minimum_required(VERSION 3.18)

project(echo-pair LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(snodec 2.0.0 REQUIRED COMPONENTS net-in-stream-legacy)

add_library(echosocketcontext STATIC EchoSocketContext.cpp EchoSocketContext.h)

target_include_directories(echosocketcontext PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(echosocketcontext PUBLIC snodec::net-in-stream-legacy)

add_executable(echoserver echoserver.cpp)

target_link_libraries(echoserver PRIVATE echosocketcontext)

add_executable(echoclient echoclient.cpp)

target_link_libraries(echoclient PRIVATE echosocketcontext)

include(GNUInstallDirs)
install(TARGETS echoserver echoclient
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
