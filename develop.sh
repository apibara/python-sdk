#!/usr/bin/env bash
export PROJECT_DIR=$(dirname "$(realpath -s "${BASH_SOURCE[0]}")")/src
nix develop --impure 
