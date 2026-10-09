# Repeat the public environment experiment at the component-ownership boundary.
add_custom_target(ch27-lab DEPENDS ch02-lab)
foreach(mode IN ITEMS consumer component)
    add_test(
        NAME exercise-ch27-${mode}
        COMMAND
            "${Python3_EXECUTABLE}"
            "${CMAKE_CURRENT_SOURCE_DIR}/../ch02/solution.py" ${mode}
            "${snodec_DIR}"
    )
    set_tests_properties(exercise-ch27-${mode} PROPERTIES TIMEOUT 180)
endforeach()
