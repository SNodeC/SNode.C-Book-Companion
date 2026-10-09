add_custom_target(ch14-lab DEPENDS semantic-logging echoserver)
add_test(
    NAME exercise-ch14-records
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/records.py"
            $<TARGET_FILE:semantic-logging>
)
add_test(
    NAME exercise-ch14-part-checkpoint
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch13/configuration.py" checkpoint
        $<TARGET_FILE:echoserver>
)
set_tests_properties(
    exercise-ch14-records exercise-ch14-part-checkpoint PROPERTIES TIMEOUT 40
)
