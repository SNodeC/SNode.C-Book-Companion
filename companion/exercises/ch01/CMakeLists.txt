add_custom_target(ch01-lab DEPENDS echoserver asio-echo)
add_test(
    NAME exercise-ch01
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            $<TARGET_FILE:echoserver> $<TARGET_FILE:asio-echo>
)
set_tests_properties(exercise-ch01 PROPERTIES TIMEOUT 40)

add_test(
    NAME exercise-ch01-independent-peers
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/independent-peers.py"
        $<TARGET_FILE:echoserver> $<TARGET_FILE:asio-echo>
)
set_tests_properties(exercise-ch01-independent-peers PROPERTIES TIMEOUT 40)
