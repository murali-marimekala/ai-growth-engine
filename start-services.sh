#!/bin/bash

# AI Growth Engine - Learning Plan Service Starter
# This script starts the web server for the AI/ML learning plan
# Handles existing processes, crashes, and provides robust service management

set -e  # Exit on any error

# Logging setup
LOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/logs"
LOG_FILE="$LOG_DIR/start-services-$(date +%Y%m%d-%H%M%S).log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
    log "INFO" "$1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    log "WARN" "$1"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    log "ERROR" "$1"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
    log "INFO" "$1"
}

log "START" "AI Growth Engine Learning Plan Service Starter started"
log "INFO" "Log file: $LOG_FILE"

# Function to kill existing server processes
kill_existing_servers() {
    local port=$1
    log "INFO" "Checking for existing servers on port $port..."

    print_info "Checking for existing servers on port $port..."

    # Find and kill any existing python http.server processes on this port
    local pids=$(lsof -ti:$port 2>/dev/null || true)
    log "DEBUG" "Found PIDs on port $port: $pids"

    if [ -n "$pids" ]; then
        print_warning "Found existing server(s) on port $port (PID: $pids)"
        log "WARN" "Terminating existing servers: $pids"
        echo "Terminating existing server(s)..."
        kill -TERM $pids 2>/dev/null || true

        # Wait for processes to terminate
        local count=0
        while [ $count -lt 10 ] && lsof -ti:$port >/dev/null 2>&1; do
            sleep 1
            count=$((count + 1))
            log "DEBUG" "Waiting for server termination... ($count/10)"
        done

        # Force kill if still running
        if lsof -ti:$port >/dev/null 2>&1; then
            print_warning "Force terminating remaining processes..."
            log "WARN" "Force terminating remaining processes"
            kill -KILL $pids 2>/dev/null || true
            sleep 2
        fi

        if lsof -ti:$port >/dev/null 2>&1; then
            print_error "Could not terminate existing server on port $port"
            log "ERROR" "Failed to terminate existing server on port $port"
            return 1
        else
            print_status "Successfully terminated existing server"
            log "INFO" "Successfully terminated existing server"
        fi
    else
        print_info "No existing servers found on port $port"
        log "INFO" "No existing servers found on port $port"
    fi

    log "INFO" "kill_existing_servers completed for port $port"
    return 0
}

# Function to start the server
start_server() {
    local port=$1
    local max_attempts=3
    local attempt=1

    log "INFO" "Starting server on port $port"

    while [ $attempt -le $max_attempts ]; do
        log "INFO" "Starting web server (attempt $attempt/$max_attempts)"
        print_info "Starting web server (attempt $attempt/$max_attempts)..."

        # Start the HTTP server in the background
        python3 -m http.server $port &
        local server_pid=$!

        log "DEBUG" "Server process started with PID: $server_pid"

        # Wait for server to start
        local wait_count=0
        while [ $wait_count -lt 10 ]; do
            if kill -0 $server_pid 2>/dev/null && curl -s --max-time 2 http://localhost:$port >/dev/null 2>&1; then
                print_status "Server started successfully on port $port (PID: $server_pid)"
                log "INFO" "Server started successfully on port $port (PID: $server_pid)"
                echo $server_pid
                return 0
            fi
            sleep 1
            wait_count=$((wait_count + 1))
            log "DEBUG" "Waiting for server to respond... ($wait_count/10)"
        done

        # If we get here, server failed to start
        print_warning "Server failed to start on attempt $attempt"
        log "WARN" "Server failed to start on attempt $attempt"

        # Kill the process if it's still running
        if kill -0 $server_pid 2>/dev/null; then
            log "DEBUG" "Terminating failed server process: $server_pid"
            kill -TERM $server_pid 2>/dev/null || true
            sleep 1
            kill -KILL $server_pid 2>/dev/null || true
        fi

        attempt=$((attempt + 1))

        if [ $attempt -le $max_attempts ]; then
            print_info "Retrying in 2 seconds..."
            log "INFO" "Retrying server startup in 2 seconds"
            sleep 2
        fi
    done

    print_error "Failed to start server after $max_attempts attempts"
    log "ERROR" "Failed to start server after $max_attempts attempts"
    return 1
}

# Function to cleanup on exit
cleanup() {
    local server_pid=$1
    if [ -n "$server_pid" ] && kill -0 $server_pid 2>/dev/null; then
        print_info "Shutting down server (PID: $server_pid)..."
        kill -TERM $server_pid 2>/dev/null || true
        sleep 2
        if kill -0 $server_pid 2>/dev/null; then
            kill -KILL $server_pid 2>/dev/null || true
        fi
    fi
    exit
}

# Main script
echo "🚀 AI Growth Engine Learning Plan Services"
echo "=========================================="
log "START" "AI Growth Engine Learning Plan Services started"

# Check for help flag
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    log "INFO" "Help requested"
    echo "AI Growth Engine - Learning Plan Service Starter"
    echo ""
    echo "Usage:"
    echo "  ./start-services.sh              # Start server in foreground"
    echo "  ./start-services.sh --daemon     # Start server as background daemon"
    echo "  ./start-services.sh --help       # Show this help"
    echo ""
    echo "Environment Variables:"
    echo "  PORT=8000                        # Port to run server on (default: 8000)"
    echo ""
    echo "The daemon mode automatically restarts the server if it crashes"
    echo "and performs health checks every 30 seconds."
    exit 0
fi

# Check for daemon mode
DAEMON_MODE=false
if [ "$1" = "--daemon" ]; then
    DAEMON_MODE=true
    log "INFO" "Daemon mode enabled"
fi

# Set the port (default to 8000, but allow override)
PORT=${PORT:-8000}
log "INFO" "Using port: $PORT"

# Validate port number
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
    print_error "Invalid port number: $PORT (must be 1024-65535)"
    log "ERROR" "Invalid port number: $PORT"
    exit 1
fi

# Change to the learning_plan directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEARNING_PLAN_DIR="$SCRIPT_DIR/learning_plan"
log "INFO" "Script directory: $SCRIPT_DIR"
log "INFO" "Learning plan directory: $LEARNING_PLAN_DIR"

if [ ! -d "$LEARNING_PLAN_DIR" ]; then
    print_error "Could not find learning_plan directory: $LEARNING_PLAN_DIR"
    log "ERROR" "Learning plan directory not found: $LEARNING_PLAN_DIR"
    exit 1
fi

# Stay in the script directory (project root) to serve learning_plan as subdirectory
cd "$SCRIPT_DIR" || {
    print_error "Could not change to script directory"
    log "ERROR" "Failed to change to script directory: $SCRIPT_DIR"
    exit 1
}

print_info "Serving from: $(pwd)"
log "INFO" "Serving from directory: $(pwd)"

# Kill any existing servers
if ! kill_existing_servers $PORT; then
    print_error "Could not clean up existing servers"
    log "ERROR" "Failed to clean up existing servers on port $PORT"
    exit 1
fi

# Start the server
SERVER_PID=$(start_server $PORT)
if [ $? -ne 0 ]; then
    print_error "Could not start the web server"
    log "ERROR" "Failed to start web server on port $PORT"
    exit 1
fi

# Set up signal handlers for cleanup
trap "cleanup $SERVER_PID" INT TERM EXIT
log "INFO" "Signal handlers set up for cleanup"

print_status "Server is running!"
log "INFO" "Server is running with PID: $SERVER_PID"
echo ""
echo "📱 Access your learning plan at: http://localhost:$PORT"
echo ""
echo "🧭 Navigation Guide:"
echo "   • Home (Year Overview): Shows 12 months"
echo "   • Click any month → Shows 4 weeks"
echo "   • Click any week → Shows 7 days"
echo "   • Click any day → Daily content & activities"
echo ""

# Try to open browser
log "INFO" "Attempting to open browser"
if command -v open >/dev/null 2>&1; then
    # macOS
    log "DEBUG" "Using macOS 'open' command"
    open "http://localhost:$PORT" 2>/dev/null || {
        print_warning "Could not open browser automatically"
        log "WARN" "Failed to open browser with 'open' command"
    }
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    log "DEBUG" "Using Linux 'xdg-open' command"
    xdg-open "http://localhost:$PORT" 2>/dev/null || {
        print_warning "Could not open browser automatically"
        log "WARN" "Failed to open browser with 'xdg-open' command"
    }
elif command -v start >/dev/null 2>&1; then
    # Windows/WSL
    log "DEBUG" "Using Windows 'start' command"
    start "http://localhost:$PORT" 2>/dev/null || {
        print_warning "Could not open browser automatically"
        log "WARN" "Failed to open browser with 'start' command"
    }
else
    print_info "Please open your browser and navigate to: http://localhost:$PORT"
    log "INFO" "No browser opener found, manual navigation required"
fi

echo ""
if [ "$DAEMON_MODE" = true ]; then
    log "INFO" "Starting daemon mode"
    print_info "Press Ctrl+C to stop the daemon"
    echo "=========================================="

    # Daemon mode: run continuously and handle crashes/restarts
    while true; do
        if [ -z "$SERVER_PID" ] || ! kill -0 $SERVER_PID 2>/dev/null; then
            if [ -n "$SERVER_PID" ]; then
                print_warning "Server process terminated unexpectedly (PID: $SERVER_PID)"
                log "WARN" "Server process terminated unexpectedly (PID: $SERVER_PID)"
            fi
            print_info "Attempting to restart server..."
            log "INFO" "Attempting to restart server"

            # Try to restart the server
            NEW_SERVER_PID=$(start_server $PORT)
            if [ $? -eq 0 ]; then
                SERVER_PID=$NEW_SERVER_PID
                print_status "Server restarted successfully (PID: $SERVER_PID)"
                log "INFO" "Server restarted successfully (PID: $SERVER_PID)"
            else
                print_error "Failed to restart server"
                log "ERROR" "Failed to restart server"
                sleep 5  # Wait before retrying
            fi
        else
            # Check server health every 30 seconds
            sleep 30
            log "DEBUG" "Performing health check"

            # Test if server is responding
            if ! curl -s --max-time 5 http://localhost:$PORT >/dev/null 2>&1; then
                print_warning "Server not responding to health check"
                log "WARN" "Server not responding to health check"
                if kill -0 $SERVER_PID 2>/dev/null; then
                    print_warning "Terminating unresponsive server process"
                    log "WARN" "Terminating unresponsive server process (PID: $SERVER_PID)"
                    kill -TERM $SERVER_PID 2>/dev/null || true
                    sleep 2
                    kill -KILL $SERVER_PID 2>/dev/null || true
                fi
                SERVER_PID=""
            else
                log "DEBUG" "Health check passed"
            fi
        fi
    done

    print_error "Daemon mode exited"
    log "ERROR" "Daemon mode exited unexpectedly"
else
    log "INFO" "Starting foreground mode"
    print_info "Server started in foreground mode"
    print_info "To run as daemon: ./start-services.sh --daemon"
    echo "=========================================="
    print_info "Server is running at: http://localhost:$PORT"
    print_info "Press Ctrl+C to stop"
    echo ""

    # Foreground mode: just show that it's running and exit
    # The server will continue running in the background
    print_status "Server started successfully! The script will now exit."
    log "INFO" "Foreground mode startup complete, script exiting"
    print_info "Server will continue running. Use Ctrl+C in another terminal to stop it."
    exit 0  # Exit without cleanup to keep server running
fi

cleanup $SERVER_PID