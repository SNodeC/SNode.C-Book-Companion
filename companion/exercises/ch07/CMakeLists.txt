find_package(
    snodec REQUIRED COMPONENTS net-in-stream-legacy net-in6-stream-legacy
                               net-un-stream-legacy
)
foreach(family IN ITEMS in in6 un)
    add_executable(endpoint-${family} family-server.cpp)
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
add_custom_target(ch07-lab DEPENDS endpoint-in endpoint-in6 endpoint-un)
add_test(
    NAME exercise-ch07-ip-families
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/families.py"
            ipv4 $<TARGET_FILE:endpoint-in> ipv6 $<TARGET_FILE:endpoint-in6>
)
add_test(
    NAME exercise-ch07-unix-path
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/families.py"
            unix $<TARGET_FILE:endpoint-un>
)
set_tests_properties(
    exercise-ch07-ip-families exercise-ch07-unix-path PROPERTIES TIMEOUT 40
)
