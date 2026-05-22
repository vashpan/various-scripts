#!/bin/bash

# download and install the latest Codex CLI release for macOS

set -euo pipefail

ASSET_NAME="codex-aarch64-apple-darwin.tar.gz"
DOWNLOAD_URL="https://github.com/openai/codex/releases/latest/download/${ASSET_NAME}"
INSTALL_DIR="/usr/local/bin"
INSTALL_PATH="${INSTALL_DIR}/codex"

TMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "${TMP_DIR}"
}

trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This installer is intended for macOS."
    exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
    echo "This installer downloads the Apple silicon build only."
    exit 1
fi

ARCHIVE_PATH="${TMP_DIR}/${ASSET_NAME}"
EXTRACT_DIR="${TMP_DIR}/extract"

mkdir -p "${EXTRACT_DIR}"

echo "Downloading Codex from ${DOWNLOAD_URL}..."

if command -v wget >/dev/null 2>&1; then
    wget --quiet --show-progress --output-document="${ARCHIVE_PATH}" "${DOWNLOAD_URL}"
else
    echo "wget is required."
    exit 1
fi

echo "Extracting archive..."
tar -xzf "${ARCHIVE_PATH}" -C "${EXTRACT_DIR}"

CODEX_BINARY=""

while IFS= read -r candidate; do
    CODEX_BINARY="${candidate}"
    break
done < <(find "${EXTRACT_DIR}" -type f -perm -111 -name "codex*")

if [[ -z "${CODEX_BINARY}" ]]; then
    echo "Could not find a Codex executable in the downloaded archive."
    exit 1
fi

echo "Installing Codex to ${INSTALL_PATH}..."

if [[ ! -d "${INSTALL_DIR}" ]]; then
    if ! mkdir -p "${INSTALL_DIR}" 2>/dev/null; then
        sudo mkdir -p "${INSTALL_DIR}"
    fi
fi

if [[ -w "${INSTALL_DIR}" ]]; then
    install -m 0755 "${CODEX_BINARY}" "${INSTALL_PATH}"
else
    sudo install -m 0755 "${CODEX_BINARY}" "${INSTALL_PATH}"
fi

echo "Installed Codex:"
"${INSTALL_PATH}" --version
