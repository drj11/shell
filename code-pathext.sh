PathExtend () {
    # Add each of "$@" to the front of $PATH, but only if not
    # already present.
    while [ $# -gt 0 ]
    do
        case $PATH in
          (*:"$1":*|"$1":*|*:"$1"|"$1") ;;
          (*) PATH=$1:$PATH ;;
        esac
        shift
    done
}
