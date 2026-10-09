# Two observations of existing canonical implementations; no application fork.
add_custom_target(ch05-lab DEPENDS endpoint-in endpoint-un echoserver)
add_test(
    NAME exercise-ch05-layer-families
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch07/families.py" ipv4
        $<TARGET_FILE:endpoint-in> unix $<TARGET_FILE:endpoint-un>
)
set_tests_properties(exercise-ch05-layer-families PROPERTIES TIMEOUT 40)
add_test(
    NAME exercise-ch05-layer-component
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch02/solution.py" component
        "${snodec_DIR}"
)
set_tests_properties(exercise-ch05-layer-component PROPERTIES TIMEOUT 180)
