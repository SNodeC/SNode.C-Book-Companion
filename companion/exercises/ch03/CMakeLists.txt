add_executable(greeting-client greeting-client.cpp)
target_compile_features(greeting-client PRIVATE cxx_std_20)
target_link_libraries(greeting-client PRIVATE echosocketcontext)
add_custom_target(ch03-lab DEPENDS greeting-client echoserver)
add_test(
    NAME exercise-ch03
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            $<TARGET_FILE:echoserver> $<TARGET_FILE:greeting-client>
)
set_tests_properties(exercise-ch03 PROPERTIES TIMEOUT 40)

add_test(
    NAME exercise-ch03-occupied-port
    COMMAND
        "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/occupied-port.py"
        $<TARGET_FILE:echoserver>
)
set_tests_properties(exercise-ch03-occupied-port PROPERTIES TIMEOUT 40)
