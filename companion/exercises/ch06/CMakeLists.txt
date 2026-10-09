find_package(snodec REQUIRED COMPONENTS core)
add_executable(deferred-work deferred-work.cpp)
target_compile_features(deferred-work PRIVATE cxx_std_20)
target_link_libraries(deferred-work PRIVATE snodec::core)
add_custom_target(ch06-lab DEPENDS deferred-work model-ownership)
add_test(NAME exercise-ch06-deferred-work COMMAND deferred-work)
add_test(NAME exercise-ch06-model-checkpoint
         COMMAND $<TARGET_FILE:model-ownership>
)
foreach(directory IN ITEMS config state runtime)
    file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${directory}")
    file(CHMOD "${CMAKE_CURRENT_BINARY_DIR}/${directory}" PERMISSIONS
         OWNER_READ OWNER_WRITE OWNER_EXECUTE
    )
endforeach()
set_property(
    TEST exercise-ch06-deferred-work
    PROPERTY ENVIRONMENT "XDG_CONFIG_HOME=${CMAKE_CURRENT_BINARY_DIR}/config"
             "XDG_STATE_HOME=${CMAKE_CURRENT_BINARY_DIR}/state"
             "XDG_RUNTIME_DIR=${CMAKE_CURRENT_BINARY_DIR}/runtime"
)
set_tests_properties(
    exercise-ch06-deferred-work exercise-ch06-model-checkpoint
    PROPERTIES TIMEOUT 10
)
