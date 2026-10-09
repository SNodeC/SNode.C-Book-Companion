add_custom_target(ch17-lab DEPENDS dispatch-lab)
foreach(mode IN ITEMS framing limits)
    add_test(
        NAME exercise-ch17-${mode}
        COMMAND
            "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/../ch18/dispatch.py" ${mode}
            $<TARGET_FILE:dispatch-lab>
    )
    set_tests_properties(exercise-ch17-${mode} PROPERTIES TIMEOUT 30)
endforeach()
