find_package(
    snodec REQUIRED COMPONENTS net-rc-stream-legacy net-l2-stream-legacy
)
add_executable(bluetooth-selectors selectors.cpp)
target_compile_features(bluetooth-selectors PRIVATE cxx_std_20)
target_link_libraries(
    bluetooth-selectors PRIVATE snodec::net-rc-stream-legacy
                                snodec::net-l2-stream-legacy
)
foreach(family IN ITEMS rc l2)
    add_executable(endpoint-${family} ../ch07/family-server.cpp)
    target_compile_features(endpoint-${family} PRIVATE cxx_std_20)
    target_compile_definitions(
        endpoint-${family}
        PRIVATE LAB_FAMILY=${family}
                LAB_HEADER="net/${family}/stream/legacy/SocketServer.h"
    )
    target_link_libraries(
        endpoint-${family} PRIVATE echosocketcontext
                                   snodec::net-${family}-stream-legacy
    )
endforeach()
add_custom_target(
    ch09-lab DEPENDS bluetooth-selectors endpoint-in endpoint-un endpoint-rc
                     endpoint-l2
)
add_test(NAME exercise-ch09-selectors COMMAND bluetooth-selectors)
add_test(
    NAME exercise-ch09-part-checkpoint
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/../ch07/families.py" ipv4
        $<TARGET_FILE:endpoint-in> unix $<TARGET_FILE:endpoint-un>
)
set_tests_properties(
    exercise-ch09-selectors exercise-ch09-part-checkpoint PROPERTIES TIMEOUT 40
)
