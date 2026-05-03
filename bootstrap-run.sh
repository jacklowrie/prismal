#!/usr/bin/env bash

# script for setting up the project to just run, NOT to
# edit/contribute/iterate/develop. If you just want
# to run/reproduce an experiment, this is your option.

set -euo pipefail

if [[ -t 1 ]]; then
    : "${RED:=\033[0;31m}"
    : "${GREEN:=\033[0;32m}"
    : "${YELLOW:=\033[0;33m}"
    : "${BLUE:=\033[0;34m}"
    : "${BOLD:=\033[1m}"
    : "${NC:=\033[0m}"
else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    BOLD=""
    NC=""
fi

info() {
    printf "%b\n" "${BLUE}${BOLD}$*${NC}"
}

success() {
    printf "%b\n" "${GREEN}${BOLD}$*${NC}"
}

warn() {
    printf "%b\n" "${YELLOW}${BOLD}$*${NC}"
}

error() {
    printf "%b\n" "${RED}${BOLD}$*${NC}"
}

if command -v uv >/dev/null 2>&1; then
    info "checking for uv... installed"
else
    info "checking for uv... not installed"
    error "uv is not installed."

    printf "\n"
    warn "Install it using one of the following methods:"
    printf "\n"
    printf "  %bmacOS / Linux (Homebrew):%b\n" "${BOLD}" "${NC}"
    printf "    brew install uv\n"
    printf "\n"
    printf "  %bWindows (WinGet):%b\n" "${BOLD}" "${NC}"
    printf "    winget install --id=astral-sh.uv -e\n"
    printf "\n"
    printf "  %bStandalone installer:%b\n" "${BOLD}" "${NC}"
    printf "    https://docs.astral.sh/uv/getting-started/installation/\n"
    printf "    %bmacOS / Linux:%b\n" "${BOLD}" "${NC}"
    printf "      curl -LsSf https://astral.sh/uv/install.sh | sh\n"
    printf "    %bWindows:%b\n" "${BOLD}" "${NC}"
    printf "      powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"\n"
    printf "\n"
    printf "If you'd like other installation options, see:\n"
    printf "  https://docs.astral.sh/uv/getting-started/installation/\n"
    exit 1
fi

info "installing project dependencies... done"
uv sync --frozen --no-dev

success "project bootstrapped successfully"
