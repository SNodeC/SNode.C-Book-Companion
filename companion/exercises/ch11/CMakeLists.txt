find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)
set(line_source
    "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/LineProtocol-Server"
)
add_executable(
    line-refusal refusal.cpp "${line_source}/LineCommandServerContext.cpp"
)
target_compile_features(line-refusal PRIVATE cxx_std_20)
target_include_directories(line-refusal PRIVATE "${line_source}")
target_link_libraries(line-refusal PRIVATE snodec::net-in-stream-legacy)
add_custom_target(ch11-lab DEPENDS line-refusal line-protocol-server)
add_test(
    NAME exercise-ch11-isolation
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch10/protocol.py" isolation
        $<TARGET_FILE:line-protocol-server>
)
add_test(
    NAME exercise-ch11-refusal
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch10/protocol.py" refusal
        $<TARGET_FILE:line-refusal>
)
set_tests_properties(
    exercise-ch11-isolation exercise-ch11-refusal PROPERTIES TIMEOUT 40
)
