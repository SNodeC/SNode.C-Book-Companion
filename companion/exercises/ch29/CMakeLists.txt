add_custom_target(ch29-lab DEPENDS ch28-lab)
foreach(mode IN ITEMS diagnosis checkpoint)
    add_test(
        NAME exercise-ch29-${mode}
        COMMAND
            "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/../ch28/installed.py" ${mode}
            "${snodec_DIR}" "$<TARGET_FILE_DIR:snodec::core>"
    )
    set_tests_properties(exercise-ch29-${mode} PROPERTIES TIMEOUT 300)
endforeach()
