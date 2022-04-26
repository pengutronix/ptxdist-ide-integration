#!/bin/bash

set -e

"{{ develop.platform }}/sysroot-host/bin/cmake" "${@}"

# The toolchain wrapper use these search paths implicitly.
# Add these fake options to ensure that a langunge server can use them as well.
cppflags="-isystem {{ develop.platform }}/sysroot-target/include -isystem {{ develop.platform }}/sysroot-target/usr/include"
filter=false
compile_commands=""

for arg in "${@}"; do
    case "${arg}" in
    -DCMAKE_EXPORT_COMPILE_COMMANDS*)
        filter=true
        ;;
    -B*)
        compile_commands="${arg#-B}/compile_commands.json"
        ;;
    esac
done

if "${filter}" && [ -e "${compile_commands}" ]; then
    sed -i \
        -e "s#\(\"command\": \"[^ ]*\(gcc\|clang\) \)#\1 ${cppflags} #" \
        -e "s#\(\"command\": \"[^ ]*++ \)#\1 ${cppflags} #" \
        "${compile_commands}"
fi
