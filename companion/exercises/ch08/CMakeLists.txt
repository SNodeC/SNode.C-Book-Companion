add_custom_target(ch08-lab DEPENDS echoserver)
add_test(
    NAME exercise-ch08-independent-peers
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch01/independent-peers.py"
        $<TARGET_FILE:echoserver>
)
add_test(
    NAME exercise-ch08-occupied-endpoint
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch03/occupied-port.py"
        $<TARGET_FILE:echoserver>
)
set_tests_properties(
    exercise-ch08-independent-peers exercise-ch08-occupied-endpoint
    PROPERTIES TIMEOUT 40
)
