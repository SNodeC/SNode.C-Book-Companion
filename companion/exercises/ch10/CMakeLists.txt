add_custom_target(ch10-lab DEPENDS line-protocol-server)
foreach(mode IN ITEMS framing limits)
    add_test(
        NAME exercise-ch10-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/protocol.py"
            ${mode} $<TARGET_FILE:line-protocol-server>
    )
    set_tests_properties(exercise-ch10-${mode} PROPERTIES TIMEOUT 40)
endforeach()
