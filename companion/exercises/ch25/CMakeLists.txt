add_custom_target(ch25-lab DEPENDS dispatch-lab echoserver)
add_test(
    NAME exercise-ch25-composition
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch18/dispatch.py" framing
        $<TARGET_FILE:dispatch-lab>
)
set_tests_properties(exercise-ch25-composition PROPERTIES TIMEOUT 30)
add_test(
    NAME exercise-ch25-consumer-trace
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch02/solution.py" consumer
        "${snodec_DIR}"
)
set_tests_properties(exercise-ch25-consumer-trace PROPERTIES TIMEOUT 180)
