#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./mac_build.sh <command> [options]

Commands:
  love        Build CLI executable (bin/love)
  app         Build macOS app bundle (bin/love.app)
  all         Build both love and app
  clean       Remove build directory

Options:
  -B, --build-dir <dir>   Build directory (default: build)
  -c, --config <cfg>      CMake build type (default: Release)
  -G, --generator <gen>   CMake generator (optional)
  -j, --jobs <n>          Parallel jobs (default: 4)
  -h, --help              Show this help

Examples:
  ./mac_build.sh love
  ./mac_build.sh app -c Release
  ./mac_build.sh all -B build-macos
EOF
}

COMMAND="${1:-}"
if [[ -z "${COMMAND}" || "${COMMAND}" == "-h" || "${COMMAND}" == "--help" ]]; then
  usage
  exit 0
fi
shift || true

BUILD_DIR="build"
CONFIG="Release"
GENERATOR=""
JOBS="4"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -B|--build-dir)
      BUILD_DIR="${2:-}"
      shift 2
      ;;
    -c|--config)
      CONFIG="${2:-}"
      shift 2
      ;;
    -G|--generator)
      GENERATOR="${2:-}"
      shift 2
      ;;
    -j|--jobs)
      JOBS="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" 1>&2
      usage 1>&2
      exit 2
      ;;
  esac
done

cmake_configure() {
  local args=("-S" "${ROOT_DIR}" "-B" "${ROOT_DIR}/${BUILD_DIR}" "-DCMAKE_BUILD_TYPE=${CONFIG}")
  if [[ -n "${GENERATOR}" ]]; then
    args+=("-G" "${GENERATOR}")
  fi
  cmake "${args[@]}"
}

cmake_build() {
  local target="$1"
  cmake --build "${ROOT_DIR}/${BUILD_DIR}" --target "${target}" -j "${JOBS}"
}

case "${COMMAND}" in
  love)
    cmake_configure
    cmake_build love
    ;;
  app)
    cmake_configure
    cmake_build love_app
    ;;
  all)
    cmake_configure
    cmake_build love
    cmake_build love_app
    ;;
  clean)
    rm -rf "${ROOT_DIR:?}/${BUILD_DIR}"
    ;;
  *)
    echo "Unknown command: ${COMMAND}" 1>&2
    usage 1>&2
    exit 2
    ;;
esac
