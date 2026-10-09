add_custom_target(ch31-lab DEPENDS minigateway-extended)
foreach(mode IN ITEMS framing mixed)
    add_test(
        NAME exercise-ch31-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/gateway.py"
            ${mode} $<TARGET_FILE:minigateway-extended>
    )
    set_tests_properties(exercise-ch31-${mode} PROPERTIES TIMEOUT 40)
endforeach()
