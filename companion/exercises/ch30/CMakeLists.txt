add_custom_target(ch30-lab DEPENDS minigateway measurement-validation)
add_test(
    NAME exercise-ch30
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
            $<TARGET_FILE:minigateway>
)
set_tests_properties(exercise-ch30 PROPERTIES TIMEOUT 40)

find_package(nlohmann_json 3.7.0 REQUIRED)
add_executable(
    measurement-validation
    validation.cpp ../../examples/MiniGateway/MeasurementModel.cpp
    ../../examples/MiniGateway/MeasurementJsonCodec.cpp
)
target_compile_features(measurement-validation PRIVATE cxx_std_20)
target_include_directories(
    measurement-validation PRIVATE ../../examples/MiniGateway
)
target_link_libraries(
    measurement-validation PRIVATE nlohmann_json::nlohmann_json
)
add_test(NAME exercise-ch30-validation COMMAND measurement-validation)
