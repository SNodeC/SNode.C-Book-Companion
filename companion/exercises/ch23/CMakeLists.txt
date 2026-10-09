add_custom_target(ch23-lab DEPENDS mqtt-role-lab mqtt-broker-lab minigateway)
add_test(
    NAME exercise-ch23-unavailable-output
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch30/solution.py"
        $<TARGET_FILE:minigateway>
)
add_test(
    NAME exercise-ch23-part-checkpoint
    COMMAND
        "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../ch21/mqtt.py"
        checkpoint $<TARGET_FILE:mqtt-role-lab> $<TARGET_FILE:mqtt-broker-lab>
        $<TARGET_FILE:minigateway>
)
set_tests_properties(
    exercise-ch23-unavailable-output exercise-ch23-part-checkpoint
    PROPERTIES TIMEOUT 60
)
