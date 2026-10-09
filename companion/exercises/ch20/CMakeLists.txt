find_package(
    snodec REQUIRED
    COMPONENTS websocket-server websocket-client http-server-express-legacy-in
               http-client net-in-stream-legacy
)
# Build linked-factory lab variants from the canonical entry points and echo
# sources.
foreach(role IN ITEMS Server Client)
    string(TOLOWER "${role}" side)
    set(example
        "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/HttpUpgrade-${role}"
    )
    set(echo
        "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/WebSocket-Echo-${role}Subprotocol"
    )
    file(READ "${example}/main.cpp" main)
    string(
        PREPEND
        main
        "#include <web/websocket/${side}/SubProtocolFactorySelector.h>\n#include \"Echo${role}Factory.h\"\n"
    )
    string(
        REPLACE
            "web::websocket::${side}::SocketContextUpgradeFactory::link();"
            "web::websocket::${side}::SocketContextUpgradeFactory::link();\n    web::websocket::${side}::SubProtocolFactorySelector::link(\"echo\", echo${role}SubProtocolFactory);"
            main
            "${main}"
    )
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/${side}.cpp" "${main}")
    add_executable(
        ws-lab-${side}
        "${CMAKE_CURRENT_BINARY_DIR}/${side}.cpp" "${echo}/Echo${role}.cpp"
        "${echo}/Echo${role}Factory.cpp"
    )
    target_compile_features(ws-lab-${side} PRIVATE cxx_std_20)
    target_include_directories(ws-lab-${side} PRIVATE "${echo}")
    target_link_libraries(ws-lab-${side} PRIVATE snodec::websocket-${side})
endforeach()
target_link_libraries(
    ws-lab-server PRIVATE snodec::http-server-express-legacy-in
)
target_link_libraries(
    ws-lab-client PRIVATE snodec::http-client snodec::net-in-stream-legacy
)
add_custom_target(ch20-lab DEPENDS ws-lab-server ws-lab-client sse-server)
add_test(
    NAME exercise-ch20-negotiation
    COMMAND
        "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
        negotiation $<TARGET_FILE:ws-lab-server> $<TARGET_FILE:ws-lab-client>
)
add_test(
    NAME exercise-ch20-part-checkpoint
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            checkpoint $<TARGET_FILE:ws-lab-server> $<TARGET_FILE:sse-server>
)
set_tests_properties(
    exercise-ch20-negotiation exercise-ch20-part-checkpoint PROPERTIES TIMEOUT
                                                                       60
)
