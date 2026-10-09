add_custom_target(ch16-lab DEPENDS echoclient tls-policy-lab)
add_test(
    NAME exercise-ch16-bounded-retry
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/recovery.py"
            retry $<TARGET_FILE:echoclient>
)
add_test(
    NAME exercise-ch16-part-checkpoint
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/recovery.py"
            checkpoint $<TARGET_FILE:echoclient> $<TARGET_FILE:tls-policy-lab>
)
set_tests_properties(
    exercise-ch16-bounded-retry exercise-ch16-part-checkpoint PROPERTIES TIMEOUT
                                                                         80
)
