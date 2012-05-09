count () { 
    case $2 in 
        *"$1"*) count "$1" "${2#*"$1"}" $(($3+1)) ;;
        *) echo ${3:-0} ;;
    esac
}
