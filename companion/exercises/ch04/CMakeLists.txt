# Reuse the existing ownership experiment and canonical EchoPair.
add_custom_target(ch04-lab DEPENDS model-instances echoserver)
add_test(NAME exercise-ch04-model-instances
         COMMAND $<TARGET_FILE:model-instances>
)
add_test(
    NAME exercise-ch04-independent-peers
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch01/independent-peers.py"
        $<TARGET_FILE:echoserver>
)
set_tests_properties(
    exercise-ch04-model-instances exercise-ch04-independent-peers
    PROPERTIES TIMEOUT 40
)
