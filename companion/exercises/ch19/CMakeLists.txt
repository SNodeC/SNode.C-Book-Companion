add_custom_target(ch19-lab DEPENDS sse-server sse-eventsource-client)
add_test(
    NAME exercise-ch19
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            $<TARGET_FILE:sse-server>
)
set_tests_properties(exercise-ch19 PROPERTIES TIMEOUT 40)

add_test(
    NAME exercise-ch19-observers
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/observers.py"
            $<TARGET_FILE:sse-server>
)
set_tests_properties(exercise-ch19-observers PROPERTIES TIMEOUT 40)
