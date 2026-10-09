find_package(
    snodec REQUIRED COMPONENTS mqtt-client-websocket websocket-client
                               http-client net-in-stream-legacy
)
set(entry
    "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/HttpUpgrade-Client/main.cpp"
)
file(READ "${entry}" main)
string(PREPEND main "void linkMqttLab();\n")
string(REPLACE "subprotocol, echo" "mqtt" main "${main}")
string(
    REPLACE
        "web::websocket::client::SocketContextUpgradeFactory::link();"
        "web::websocket::client::SocketContextUpgradeFactory::link();\n    linkMqttLab();"
        main
        "${main}"
)
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/client.cpp" "${main}")
add_executable(mqtt-ws-lab "${CMAKE_CURRENT_BINARY_DIR}/client.cpp" factory.cpp)
target_compile_features(mqtt-ws-lab PRIVATE cxx_std_20)
target_include_directories(
    mqtt-ws-lab
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/MQTT-ClientRole"
)
target_link_libraries(
    mqtt-ws-lab
    PRIVATE mqtt-client-role snodec::mqtt-client snodec::mqtt-client-websocket
            snodec::websocket-client snodec::http-client
            snodec::net-in-stream-legacy
)
add_custom_target(ch22-lab DEPENDS mqtt-ws-lab)
foreach(mode IN ITEMS binary text)
    add_test(
        NAME exercise-ch22-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/adapter.py"
            ${mode} $<TARGET_FILE:mqtt-ws-lab>
    )
    set_tests_properties(exercise-ch22-${mode} PROPERTIES TIMEOUT 40)
endforeach()
