#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a Git repository. Please run this script in your project root.${NC}"
    exit 1
fi

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python not found! Please install Python 3.${NC}"
    exit 1
fi

echo -e "${BLUE}Installing AI Git-Hook Reviewer...${NC}"

if [ -L ".git-reviewer" ]; then
    echo -e "${RED}Error: '.git-reviewer' is a symbolic link. Please remove it manually to prevent unsafe deletion.${NC}"
    exit 1
elif [ -d ".git-reviewer" ]; then
    echo -e "${BLUE}Updating existing installation...${NC}"
    rm -rf .git-reviewer
fi

git clone -q https://github.com/quilix11/git-reviewer.git .git-reviewer

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to clone the repository.${NC}"
    exit 1
fi

cd .git-reviewer
exec < /dev/tty
$PYTHON_CMD install.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Installation complete! AI Reviewer is now active as a pre-commit hook.${NC}"
else
    echo -e "${RED}Installation failed.${NC}"
    exit 1
fi