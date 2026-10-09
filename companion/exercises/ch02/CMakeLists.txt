# Reuse the canonical program; each lab independently configures an external build.
add_custom_target(ch02-lab DEPENDS echoserver echoclient)
foreach(mode IN ITEMS consumer component)
    add_test(
        NAME exercise-ch02-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            ${mode} "${snodec_DIR}"
    )
    set_tests_properties(exercise-ch02-${mode} PROPERTIES TIMEOUT 180)
endforeach()
