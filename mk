#!/bin/sh

rj () {
    ./rj.py "$@" > rendered/"$1"
}

mkdir -p rendered

rj box-chu
rj chapter-redirect
