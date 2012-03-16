_chu () {
    cd "$2/$1" 2>&- && return
    if [ -z "$2" ] ; then
        return 99
    fi
    _chu "$1" "${2%/*}"
}

chu () {
    _chu "$1" "$(pwd)" || cd "$1"
}

