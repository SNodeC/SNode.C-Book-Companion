find_package(
    snodec REQUIRED COMPONENTS mqtt-client mqtt-server net-in-stream-legacy
)
set(role "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/MQTT-ClientRole")
add_executable(mqtt-role-lab client.cpp)
target_compile_features(mqtt-role-lab PRIVATE cxx_std_20)
target_include_directories(mqtt-role-lab PRIVATE "${role}")
target_link_libraries(
    mqtt-role-lab PRIVATE mqtt-client-role snodec::mqtt-client
                          snodec::net-in-stream-legacy
)
add_executable(mqtt-broker-lab broker.cpp)
target_compile_features(mqtt-broker-lab PRIVATE cxx_std_20)
target_link_libraries(
    mqtt-broker-lab PRIVATE snodec::mqtt-server snodec::net-in-stream-legacy
)
add_custom_target(ch21-lab DEPENDS mqtt-role-lab mqtt-broker-lab)
foreach(mode IN ITEMS wire delivery)
    add_test(
        NAME exercise-ch21-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/mqtt.py"
            ${mode} $<TARGET_FILE:mqtt-role-lab> $<TARGET_FILE:mqtt-broker-lab>
    )
    set_tests_properties(exercise-ch21-${mode} PROPERTIES TIMEOUT 40)
endforeach()
