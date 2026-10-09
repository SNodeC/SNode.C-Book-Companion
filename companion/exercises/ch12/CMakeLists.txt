find_package(snodec REQUIRED COMPONENTS net-un-stream-legacy)
set(line_source
    "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/LineProtocol-Server"
)
# Apply exactly the worked carrier edits to the canonical entry point at
# configure time.
set_property(
    DIRECTORY
    APPEND
    PROPERTY CMAKE_CONFIGURE_DEPENDS "${line_source}/main.cpp"
)
file(READ "${line_source}/main.cpp" unix_main)
string(REPLACE "net/in/stream/legacy/SocketServer.h"
               "net/un/stream/legacy/SocketServer.h" unix_main "${unix_main}"
)
string(REPLACE "net::in::stream::legacy" "net::un::stream::legacy" unix_main
               "${unix_main}"
)
string(REPLACE "8090," "\"/tmp/line-transfer.sock\"," unix_main "${unix_main}")
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/unix-main.cpp" "${unix_main}")
add_executable(
    line-unix "${CMAKE_CURRENT_BINARY_DIR}/unix-main.cpp"
              "${line_source}/LineCommandServerContext.cpp"
)
target_compile_features(line-unix PRIVATE cxx_std_20)
target_include_directories(line-unix PRIVATE "${line_source}")
target_link_libraries(line-unix PRIVATE snodec::net-un-stream-legacy)
add_custom_target(ch12-lab DEPENDS line-unix line-protocol-server)
add_test(
    NAME exercise-ch12-part-checkpoint
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch10/protocol.py" transfer
        $<TARGET_FILE:line-protocol-server> $<TARGET_FILE:line-unix>
)
add_test(
    NAME exercise-ch12-endpoint-failure
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch10/protocol.py" endpoint-failure
        $<TARGET_FILE:line-unix>
)
set_tests_properties(
    exercise-ch12-part-checkpoint exercise-ch12-endpoint-failure
    PROPERTIES TIMEOUT 40
)
