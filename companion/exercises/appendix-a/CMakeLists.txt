# Reuse the external consumer and the canonical carrier-extension experiment.
add_custom_target(appendix-a-lab DEPENDS ch02-lab ch12-lab)
add_test(
    NAME exercise-appendix-a-source-consumer
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch02/solution.py" consumer
        "${snodec_DIR}"
)
add_test(
    NAME exercise-appendix-a-carrier-extension
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch10/protocol.py" transfer
        $<TARGET_FILE:line-protocol-server> $<TARGET_FILE:line-unix>
)
set_tests_properties(exercise-appendix-a-source-consumer PROPERTIES TIMEOUT 180)
set_tests_properties(
    exercise-appendix-a-carrier-extension PROPERTIES TIMEOUT 40
)
