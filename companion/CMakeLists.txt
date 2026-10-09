cmake_minimum_required(VERSION 3.14)

# Private-prefix exercise binaries must resolve indirect SNode.C dependencies
# too. Match the installed-consumer lifecycle lab's inherited RPATH policy on
# Linux.
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    add_link_options("LINKER:--disable-new-dtags")
endif()

add_subdirectory(examples)
add_subdirectory(exercises)
