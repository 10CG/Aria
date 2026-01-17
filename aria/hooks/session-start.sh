#!/bin/bash
# Aria Session Start Hook
# 在 Claude Code 会话开始时执行环境检查和配置加载

set -euo pipefail

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOKS_CONFIG="$SCRIPT_DIR/hooks.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 主函数
main() {
    echo ""
    log_info "Aria Hooks - Session Start"
    echo "================================"

    # 1. 检查 Git 状态
    log_info "Checking Git status..."
    if [ -d "$PROJECT_ROOT/.git" ]; then
        if git -C "$PROJECT_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
            BRANCH=$(git -C "$PROJECT_ROOT" branch --show-current 2>/dev/null || echo "HEAD")
            log_success "Git repository detected (branch: $BRANCH)"

            # 检查是否有未提交的变更
            if [ -n "$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null)" ]; then
                log_warn "Uncommitted changes detected"
            fi
        fi
    fi

    # 2. 检查子模块状态
    log_info "Checking submodules..."
    if [ -f "$PROJECT_ROOT/.gitmodules" ]; then
        if command_exists git; then
            SUBMODULE_OUTPUT=$(git -C "$PROJECT_ROOT" submodule status 2>/dev/null || true)
            if echo "$SUBMODULE_OUTPUT" | grep -q "^-"; then
                log_warn "Some submodules are not initialized"
            else
                log_success "Submodules initialized"
            fi
        fi
    fi

    # 3. 检查 Python 环境
    log_info "Checking Python environment..."
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python $PYTHON_VERSION"
    elif command_exists python; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        log_success "Python $PYTHON_VERSION"
    else
        log_warn "Python not found"
    fi

    # 4. 检查 Node.js 环境
    log_info "Checking Node.js environment..."
    if command_exists node; then
        NODE_VERSION=$(node --version 2>/dev/null)
        log_success "Node.js $NODE_VERSION"
    else
        log_warn "Node.js not found"
    fi

    # 5. 检查 Flutter 环境 (Mobile)
    log_info "Checking Flutter environment..."
    if command_exists flutter; then
        FLUTTER_VERSION=$(flutter --version 2>/dev/null | head -n 1)
        log_success "$FLUTTER_VERSION"
    else
        log_info "Flutter not found (skip for non-mobile work)"
    fi

    # 6. 加载项目环境变量
    log_info "Loading environment variables..."
    if [ -f "$PROJECT_ROOT/.env" ]; then
        log_warn ".env file found (consider using .env.example)"
    fi

    # 7. 检查 Hooks 配置
    if [ -f "$HOOKS_CONFIG" ]; then
        log_success "Hooks configuration loaded"
    else
        log_warn "Hooks configuration not found"
    fi

    echo ""
    log_success "Session start checks completed"
    echo ""
}

# 执行主函数
main "$@"
