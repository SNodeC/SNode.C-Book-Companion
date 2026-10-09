cmake_minimum_required(VERSION 3.18)
project(SemanticLogging LANGUAGES CXX)

# core is a supported requested component; logger is loaded through its graph.
find_package(snodec 2.0.0 REQUIRED COMPONENTS core)
add_executable(semantic-logging main.cpp)
target_compile_features(semantic-logging PRIVATE cxx_std_20)
target_link_libraries(semantic-logging PRIVATE snodec::logger)

include(GNUInstallDirs)
install(TARGETS semantic-logging RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
