find_package(snodec REQUIRED COMPONENTS net-in-stream-tls)
find_program(OPENSSL_EXECUTABLE openssl REQUIRED)
add_executable(tls-policy-lab tls-runtime.cpp)
target_compile_features(tls-policy-lab PRIVATE cxx_std_20)
target_link_libraries(tls-policy-lab PRIVATE snodec::net-in-stream-tls)
# Apply the chapter's wrapper substitution to the canonical EchoPair entry
# point.
set(echo_source "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/EchoPair")
set_property(
    DIRECTORY
    APPEND
    PROPERTY CMAKE_CONFIGURE_DEPENDS "${echo_source}/echoserver.cpp"
)
file(READ "${echo_source}/echoserver.cpp" tls_main)
string(REPLACE "net/in/stream/legacy/SocketServer.h"
               "net/in/stream/tls/SocketServer.h" tls_main "${tls_main}"
)
string(REPLACE "net::in::stream::legacy" "net::in::stream::tls" tls_main
               "${tls_main}"
)
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/tls-main.cpp" "${tls_main}")
add_executable(tls-echo "${CMAKE_CURRENT_BINARY_DIR}/tls-main.cpp")
target_compile_features(tls-echo PRIVATE cxx_std_20)
target_link_libraries(
    tls-echo PRIVATE echosocketcontext snodec::net-in-stream-tls
)
add_custom_target(ch15-lab DEPENDS tls-policy-lab tls-echo)
add_test(NAME exercise-ch15-trust-identity
         COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tls.py"
                 policy $<TARGET_FILE:tls-policy-lab> "${OPENSSL_EXECUTABLE}"
)
add_test(NAME exercise-ch15-secure-echo
         COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tls.py"
                 echo $<TARGET_FILE:tls-echo> "${OPENSSL_EXECUTABLE}"
)
set_tests_properties(
    exercise-ch15-trust-identity exercise-ch15-secure-echo PROPERTIES TIMEOUT
                                                                      60
)
