cmake_minimum_required(VERSION 3.14)

project(MariaDBMinimal LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(snodec 2.0.0 REQUIRED COMPONENTS db-mariadb)

add_executable(mariadb-minimal main.cpp)

target_link_libraries(mariadb-minimal PRIVATE snodec::db-mariadb)

install(
    TARGETS mariadb-minimal
    COMPONENT MariaDBMinimal
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-mariadb-minimal
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component
            MariaDBMinimal
    DEPENDS mariadb-minimal
    COMMENT "Installing mariadb-minimal"
    VERBATIM
)
