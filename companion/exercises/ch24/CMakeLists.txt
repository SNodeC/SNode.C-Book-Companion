find_package(snodec REQUIRED COMPONENTS db-mariadb)
set(entry "${CMAKE_CURRENT_SOURCE_DIR}/../../examples/MariaDB-Minimal/main.cpp")
set_property(
    DIRECTORY
    APPEND
    PROPERTY CMAKE_CONFIGURE_DEPENDS "${entry}"
)
file(READ "${entry}" main)
string(PREPEND main "#include <cstdlib>\n")
string(
    REPLACE
        "core::SNodeC::init(argc, argv);"
        "if (!std::getenv(\"BOOK_DB_SOCKET\") || !std::getenv(\"BOOK_DB_SQL\")) return 2;\n    core::SNodeC::init(argc, argv);"
        main
        "${main}"
)
string(REPLACE ".username = \"snodec\"" ".username = \"root\"" main "${main}")
string(REPLACE ".password = \"<password>\"" ".password = \"\"" main "${main}")
string(REPLACE ".database = \"snodec\"" ".database = \"book\"" main "${main}")
string(REPLACE ".socket = \"\"" ".socket = std::getenv(\"BOOK_DB_SOCKET\")"
               main "${main}"
)
string(
    REPLACE
        "\"INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)\""
        "std::getenv(\"BOOK_DB_SQL\")"
        main
        "${main}"
)
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/client.cpp" "${main}")
add_executable(persistence-lab "${CMAKE_CURRENT_BINARY_DIR}/client.cpp")
target_compile_features(persistence-lab PRIVATE cxx_std_20)
target_link_libraries(persistence-lab PRIVATE snodec::db-mariadb)
add_custom_target(ch24-lab DEPENDS persistence-lab)
foreach(mode IN ITEMS durable error)
    add_test(
        NAME exercise-ch24-${mode}
        COMMAND
            "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/database.py"
            ${mode} $<TARGET_FILE:persistence-lab>
    )
    set_tests_properties(
        exercise-ch24-${mode} PROPERTIES TIMEOUT 90 LABELS equipped
    )
endforeach()
