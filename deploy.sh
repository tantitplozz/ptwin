#!/bin/bash

# 🔥 GOD-TIER PhantomAutoBuyBot - Production Deployment Script
# ===========================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ptwin"
DOCKER_IMAGE="god-tier-phantom-bot"
CONTAINER_NAME="phantom-autobuy-bot"
NETWORK_NAME="phantom-network"
DATA_DIR="/opt/phantom-data"
LOG_DIR="/var/log/phantom"

# Function to print colored output
print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
print_header() { echo -e "${PURPLE}🔥 $1${NC}"; }

# Parse command line arguments
DEPLOYMENT_TYPE="production"
SKIP_BUILD=false
SKIP_TESTS=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dev|--development)
            DEPLOYMENT_TYPE="development"
            shift
            ;;
        --staging)
            DEPLOYMENT_TYPE="staging"
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --dev, --development    Deploy in development mode"
            echo "  --staging              Deploy in staging mode"
            echo "  --skip-build           Skip Docker image build"
            echo "  --skip-tests           Skip health checks"
            echo "  --dry-run              Show what would be done"
            echo "  -h, --help             Show this help"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_header "GOD-TIER PhantomAutoBuyBot Deployment"
print_info "Deployment type: $DEPLOYMENT_TYPE"
print_info "Skip build: $SKIP_BUILD"
print_info "Skip tests: $SKIP_TESTS"
print_info "Dry run: $DRY_RUN"
echo "=================================================="

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker."
        exit 1
    fi
    print_status "Docker found"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_warning "docker-compose not found, using docker compose"
    fi
    
    # Check if running as root for production
    if [[ "$DEPLOYMENT_TYPE" == "production" && $EUID -ne 0 ]]; then
        print_warning "Production deployment recommended to run as root"
    fi
    
    # Check .env file
    if [[ ! -f ".env" ]]; then
        print_error ".env file not found. Please copy .env.template to .env and configure it."
        exit 1
    fi
    print_status "Configuration file found"
}

# Create necessary directories
setup_directories() {
    print_info "Setting up directories..."
    
    if [[ "$DRY_RUN" == "false" ]]; then
        sudo mkdir -p "$DATA_DIR"/{logs,screenshots,data,backups}
        sudo mkdir -p "$LOG_DIR"
        sudo chown -R $USER:$USER "$DATA_DIR" "$LOG_DIR" 2>/dev/null || true
    fi
    
    print_status "Directories created"
}

# Build Docker image
build_image() {
    if [[ "$SKIP_BUILD" == "true" ]]; then
        print_warning "Skipping Docker build"
        return
    fi
    
    print_info "Building Docker image..."
    
    if [[ "$DRY_RUN" == "false" ]]; then
        docker build -t "$DOCKER_IMAGE:latest" -f Dockerfile .
        
        # Tag with deployment type
        docker tag "$DOCKER_IMAGE:latest" "$DOCKER_IMAGE:$DEPLOYMENT_TYPE"
        
        # Tag with timestamp
        TIMESTAMP=$(date +%Y%m%d-%H%M%S)
        docker tag "$DOCKER_IMAGE:latest" "$DOCKER_IMAGE:$TIMESTAMP"
    fi
    
    print_status "Docker image built"
}

# Create Docker network
setup_network() {
    print_info "Setting up Docker network..."
    
    if [[ "$DRY_RUN" == "false" ]]; then
        docker network create "$NETWORK_NAME" 2>/dev/null || true
    fi
    
    print_status "Network configured"
}

# Generate docker-compose file
generate_compose_file() {
    print_info "Generating docker-compose configuration..."
    
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  phantom-bot:
    image: ${DOCKER_IMAGE}:${DEPLOYMENT_TYPE}
    container_name: ${CONTAINER_NAME}
    restart: unless-stopped
    environment:
      - DEPLOYMENT_TYPE=${DEPLOYMENT_TYPE}
    env_file:
      - .env
    volumes:
      - ${DATA_DIR}/logs:/app/logs
      - ${DATA_DIR}/screenshots:/app/screenshots
      - ${DATA_DIR}/data:/app/data
      - ${DATA_DIR}/backups:/app/backups
    ports:
      - "8686:8686"  # Monitor WebSocket
      - "8687:8687"  # Dashboard
    networks:
      - ${NETWORK_NAME}
    healthcheck:
      test: ["CMD", "python3", "health_check.py"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: phantom-redis
    restart: unless-stopped
    volumes:
      - ${DATA_DIR}/redis:/data
    networks:
      - ${NETWORK_NAME}
    command: redis-server --appendonly yes

  nginx:
    image: nginx:alpine
    container_name: phantom-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ${DATA_DIR}/ssl:/etc/ssl/certs:ro
    networks:
      - ${NETWORK_NAME}
    depends_on:
      - phantom-bot

networks:
  ${NETWORK_NAME}:
    external: true

volumes:
  phantom-data:
    driver: local
EOF

    print_status "Docker Compose configuration generated"
}

# Generate nginx configuration
generate_nginx_config() {
    print_info "Generating nginx configuration..."
    
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream phantom_dashboard {
        server phantom-bot:8687;
    }
    
    upstream phantom_monitor {
        server phantom-bot:8686;
    }
    
    server {
        listen 80;
        server_name _;
        
        # Redirect HTTP to HTTPS in production
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name _;
        
        # SSL configuration (add your certificates)
        # ssl_certificate /etc/ssl/certs/cert.pem;
        # ssl_certificate_key /etc/ssl/certs/key.pem;
        
        # Dashboard
        location / {
            proxy_pass http://phantom_dashboard;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # WebSocket monitoring
        location /ws {
            proxy_pass http://phantom_monitor;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    print_status "Nginx configuration generated"
}

# Deploy services
deploy_services() {
    print_info "Deploying services..."
    
    if [[ "$DRY_RUN" == "false" ]]; then
        # Stop existing containers
        docker-compose down 2>/dev/null || true
        
        # Start services
        docker-compose up -d
        
        # Wait for services to be ready
        print_info "Waiting for services to start..."
        sleep 10
    fi
    
    print_status "Services deployed"
}

# Run health checks
run_health_checks() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        print_warning "Skipping health checks"
        return
    fi
    
    print_info "Running health checks..."
    
    if [[ "$DRY_RUN" == "false" ]]; then
        # Check container health
        if docker ps | grep -q "$CONTAINER_NAME"; then
            print_status "Container is running"
        else
            print_error "Container is not running"
            return 1
        fi
        
        # Check application health
        sleep 5
        if docker exec "$CONTAINER_NAME" python3 health_check.py; then
            print_status "Application health check passed"
        else
            print_warning "Application health check failed"
        fi
        
        # Check dashboard accessibility
        if curl -f http://localhost:8687 >/dev/null 2>&1; then
            print_status "Dashboard is accessible"
        else
            print_warning "Dashboard is not accessible"
        fi
    fi
    
    print_status "Health checks completed"
}

# Setup monitoring and alerts
setup_monitoring() {
    print_info "Setting up monitoring..."
    
    # Create monitoring script
    cat > monitor.sh << 'EOF'
#!/bin/bash

# Monitor script for GOD-TIER PhantomAutoBuyBot
CONTAINER_NAME="phantom-autobuy-bot"
LOG_FILE="/var/log/phantom/monitor.log"

check_container() {
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo "$(date): Container $CONTAINER_NAME is not running, restarting..." >> "$LOG_FILE"
        docker-compose restart phantom-bot
        return 1
    fi
    return 0
}

check_health() {
    if ! docker exec "$CONTAINER_NAME" python3 health_check.py >/dev/null 2>&1; then
        echo "$(date): Health check failed, restarting container..." >> "$LOG_FILE"
        docker-compose restart phantom-bot
        return 1
    fi
    return 0
}

# Run checks
check_container
check_health

echo "$(date): Monitoring check completed" >> "$LOG_FILE"
EOF

    chmod +x monitor.sh
    
    # Setup cron job for monitoring (every 5 minutes)
    if [[ "$DRY_RUN" == "false" && "$DEPLOYMENT_TYPE" == "production" ]]; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/monitor.sh") | crontab -
        print_status "Monitoring cron job installed"
    fi
    
    print_status "Monitoring setup completed"
}

# Setup log rotation
setup_log_rotation() {
    print_info "Setting up log rotation..."
    
    if [[ "$DRY_RUN" == "false" && "$DEPLOYMENT_TYPE" == "production" ]]; then
        cat > /etc/logrotate.d/phantom-bot << EOF
${LOG_DIR}/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF
        print_status "Log rotation configured"
    fi
}

# Create backup script
create_backup_script() {
    print_info "Creating backup script..."
    
    cat > backup.sh << 'EOF'
#!/bin/bash

# Backup script for GOD-TIER PhantomAutoBuyBot
BACKUP_DIR="/opt/phantom-data/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="phantom-backup-$TIMESTAMP.tar.gz"

echo "Creating backup: $BACKUP_FILE"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude="$BACKUP_DIR" \
    /opt/phantom-data \
    /var/log/phantom \
    $(pwd)/.env \
    $(pwd)/docker-compose.yml

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t phantom-backup-*.tar.gz | tail -n +8 | xargs rm -f

echo "Backup completed: $BACKUP_FILE"
EOF

    chmod +x backup.sh
    
    # Setup daily backup cron job
    if [[ "$DRY_RUN" == "false" && "$DEPLOYMENT_TYPE" == "production" ]]; then
        (crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup.sh") | crontab -
        print_status "Backup cron job installed"
    fi
    
    print_status "Backup script created"
}

# Print deployment summary
print_summary() {
    print_header "Deployment Summary"
    echo "=================================================="
    print_info "Deployment type: $DEPLOYMENT_TYPE"
    print_info "Container name: $CONTAINER_NAME"
    print_info "Data directory: $DATA_DIR"
    print_info "Log directory: $LOG_DIR"
    echo ""
    print_info "Services:"
    print_info "  - Dashboard: http://localhost:8687"
    print_info "  - Monitor: http://localhost:8686"
    print_info "  - Nginx: http://localhost (if configured)"
    echo ""
    print_info "Management commands:"
    print_info "  - View logs: docker-compose logs -f phantom-bot"
    print_info "  - Restart: docker-compose restart phantom-bot"
    print_info "  - Stop: docker-compose down"
    print_info "  - Health check: docker exec $CONTAINER_NAME python3 health_check.py"
    echo ""
    print_status "🔥 GOD-TIER PhantomAutoBuyBot deployed successfully!"
}

# Main deployment flow
main() {
    check_prerequisites
    setup_directories
    build_image
    setup_network
    generate_compose_file
    generate_nginx_config
    deploy_services
    run_health_checks
    setup_monitoring
    setup_log_rotation
    create_backup_script
    print_summary
}

# Run main function
main "$@"