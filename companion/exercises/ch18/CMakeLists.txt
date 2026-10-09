find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in)
add_executable(dispatch-lab dispatch.cpp)
target_compile_features(dispatch-lab PRIVATE cxx_std_20)
target_link_libraries(
    dispatch-lab PRIVATE snodec::http-server-express-legacy-in
)
add_custom_target(ch18-lab DEPENDS dispatch-lab)
foreach(mode IN ITEMS order stop)
    add_test(
        NAME exercise-ch18-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/dispatch.py"
            ${mode} $<TARGET_FILE:dispatch-lab>
    )
    set_tests_properties(exercise-ch18-${mode} PROPERTIES TIMEOUT 30)
endforeach()
