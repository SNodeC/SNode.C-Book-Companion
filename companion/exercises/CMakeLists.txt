find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(snodec 2.0.0 REQUIRED COMPONENTS core)
# Both WebSocket labs derive entry points from these canonical sources.
foreach(role IN ITEMS Server Client)
    get_filename_component(
        entry
        "${CMAKE_CURRENT_SOURCE_DIR}/../examples/HttpUpgrade-${role}/main.cpp"
        REALPATH
    )
    set_property(
        DIRECTORY
        APPEND
        PROPERTY CMAKE_CONFIGURE_DEPENDS "${entry}"
    )
endforeach()
foreach(
    chapter IN
    ITEMS ch01
          ch02
          ch03
          ch04
          ch05
          ch06
          ch07
          ch08
          ch09
          ch10
          ch11
          ch12
          ch13
          ch14
          ch15
          ch16
          ch17
          ch18
          ch19
          ch20
          ch21
          ch22
          ch23
          ch24
          ch25
          ch26
          ch27
          ch28
          ch29
          ch30
          ch31
          ch32
          appendix-a
)
    add_subdirectory(${chapter})
    add_dependencies(all-examples ${chapter}-lab)
endforeach()
