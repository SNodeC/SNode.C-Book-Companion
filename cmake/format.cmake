# SNode.C - A Slim Toolkit for Network Communication
# Copyright (C) Volker Christian <me@vchrist.at>
#               2020, 2021, 2022, 2023, 2024, 2025, 2026
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Custom target to trigger clang-format and cmake-format

# Remove strings matching given regular expression from a list. @param(in,out)
# aItems Reference of a list variable to filter. @param aRegEx Value of regular
# expression to match.
function(filter_items aItems aRegEx)
    # For each item in our list
    foreach(item ${${aItems}})
        # Check if our items matches our regular expression
        if("${item}" MATCHES ${aRegEx})
            # Remove current item from our list
            list(REMOVE_ITEM ${aItems} ${item})
        endif("${item}" MATCHES ${aRegEx})
    endforeach(item)
    # Provide output parameter
    set(${aItems}
        ${${aItems}}
        PARENT_SCOPE
    )
endfunction(filter_items)

# Exclude generated trees from both formatters, including this CMake build.
set(BOOK_FORMAT_EXCLUDE
    "/(build[^/]*|cmake-build[^/]*|_deps|CMakeFiles|out|install|external|snode[.]c)/"
)
file(GLOB_RECURSE BOOK_FORMAT_CACHES "${CMAKE_SOURCE_DIR}/CMakeCache.txt")
list(APPEND BOOK_FORMAT_CACHES "${CMAKE_BINARY_DIR}/CMakeCache.txt")
foreach(BOOK_FORMAT_CACHE IN LISTS BOOK_FORMAT_CACHES)
    get_filename_component(BOOK_FORMAT_BINARY "${BOOK_FORMAT_CACHE}" DIRECTORY)
    if(NOT BOOK_FORMAT_BINARY STREQUAL CMAKE_SOURCE_DIR)
        string(REGEX REPLACE "([][+.*()^$?|\\])" "\\\\\\1"
                             BOOK_FORMAT_BINARY_REGEX "${BOOK_FORMAT_BINARY}"
        )
        string(APPEND BOOK_FORMAT_EXCLUDE "|^${BOOK_FORMAT_BINARY_REGEX}/")
    endif()
endforeach()

add_custom_target(format DEPENDS format-cmds)
add_custom_command(
    OUTPUT format-cmds
    COMMENT "Auto formatting of all source and all cmake files"
)

include(clang-format)
include(cmake-format)

if(CLANG_FORMAT AND CMAKE_FORMAT)
    add_custom_target(
        format-check
        COMMAND ${CLANG_FORMAT} --version
        COMMAND ${CMAKE_FORMAT} --version
        COMMAND ${CLANG_FORMAT} --dry-run --Werror ${CHECK_CXX_SOURCE_FILES}
        COMMAND ${CMAKE_FORMAT} --check ${CMAKELISTS_TXT_FILES}
        COMMENT "Checking source and CMake formatting"
        VERBATIM
    )
else()
    add_custom_target(
        format-check
        COMMAND ${CMAKE_COMMAND} -E echo
                "format-check requires clang-format and cmake-format"
        COMMAND ${CMAKE_COMMAND} -E false
        VERBATIM
    )
endif()
