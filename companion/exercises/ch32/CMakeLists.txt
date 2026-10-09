add_executable(
    model-ownership model-ownership.cpp
                    ../../examples/MiniGateway/MeasurementModel.cpp
)
target_compile_features(model-ownership PRIVATE cxx_std_20)
target_include_directories(model-ownership PRIVATE ../../examples/MiniGateway)
add_custom_target(ch32-lab DEPENDS model-ownership model-instances)
add_custom_target(part-xi-checkpoint DEPENDS ch30-lab ch31-lab ch32-lab)
add_test(NAME exercise-ch32 COMMAND model-ownership)

add_executable(
    model-instances model-instances.cpp
                    ../../examples/MiniGateway/MeasurementModel.cpp
)
target_compile_features(model-instances PRIVATE cxx_std_20)
target_include_directories(model-instances PRIVATE ../../examples/MiniGateway)
add_test(NAME exercise-ch32-model-instances COMMAND model-instances)
