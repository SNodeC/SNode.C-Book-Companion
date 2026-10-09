add_custom_target(
    ch26-lab DEPENDS persistence-lab minigateway mqtt-role-lab mqtt-broker-lab
)
add_test(
    NAME exercise-ch26-part-checkpoint
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch24/database.py" checkpoint
        $<TARGET_FILE:persistence-lab> $<TARGET_FILE:minigateway>
)
set_tests_properties(
    exercise-ch26-part-checkpoint PROPERTIES TIMEOUT 120 LABELS equipped
)
add_test(
    NAME exercise-ch26-publication-trace
    COMMAND
        "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../ch21/mqtt.py"
        delivery $<TARGET_FILE:mqtt-role-lab> $<TARGET_FILE:mqtt-broker-lab>
)
set_tests_properties(exercise-ch26-publication-trace PROPERTIES TIMEOUT 40)
