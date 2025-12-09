# Production Deployment Guide for api.mypisang.info

## Prerequisites

1. **Server Setup**
   - Ubuntu/CentOS server with Docker and Docker Compose installed
   - Domain `api.mypisang.info` pointing to your server IP
   - SSL certificate for `api.mypisang.info`

2. **SSL Certificate Setup**
   ```bash
   # Create SSL directory
   mkdir -p ssl
   
   # Option 1: Let's Encrypt (Recommended)
   sudo apt install certbot
   sudo certbot certonly --standalone -d api.mypisang.info
   sudo cp /etc/letsencrypt/live/api.mypisang.info/fullchain.pem ssl/cert.pem
   sudo cp /etc/letsencrypt/live/api.mypisang.info/privkey.pem ssl/key.pem
   
   # Option 2: Upload your own certificates
   # Place your certificate files as:
   # - ssl/cert.pem (full certificate chain)
   # - ssl/key.pem (private key)
   ```

## Deployment Steps

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd apiendpoint
```

### 2. Configure Environment
```bash
# Create production environment file
cat > .env << EOF
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
HOST=0.0.0.0
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

### 3. Deploy with Docker Compose
```bash
# Build and start in production mode
docker-compose --profile production up -d --build

# Verify services are running
docker-compose ps

# Check logs
docker-compose logs -f
```

### 4. Verify Deployment
```bash
# Test HTTP (should redirect to HTTPS)
curl -I http://api.mypisang.info

# Test HTTPS API
curl -X POST https://api.mypisang.info/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@company.com", "password": "password123"}'

# Test health endpoint
curl https://api.mypisang.info/health
```

## Production URLs

- **API Base URL**: `https://api.mypisang.info/api/v1`
- **Health Check**: `https://api.mypisang.info/health`
- **Root**: `https://api.mypisang.info/`

## Production Features Enabled

- ✅ HTTPS with SSL termination
- ✅ HTTP to HTTPS redirect
- ✅ Nginx reverse proxy with rate limiting
- ✅ Security headers
- ✅ CORS configured for mypisang.info domains
- ✅ Health checks and monitoring
- ✅ Production Flask settings (debug=false)

## Monitoring and Maintenance

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f attendance-api
docker-compose logs -f nginx
```

### Scale Application
```bash
# Run multiple API instances
docker-compose up -d --scale attendance-api=3
```

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose --profile production up -d --build
```

### SSL Certificate Renewal (Let's Encrypt)
```bash
# Renew certificate
sudo certbot renew

# Copy renewed certificates
sudo cp /etc/letsencrypt/live/api.mypisang.info/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/api.mypisang.info/privkey.pem ssl/key.pem

# Restart nginx to load new certificates
docker-compose restart nginx
```

## Security Considerations

1. **Firewall Rules**
   ```bash
   # Allow only necessary ports
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable
   ```

2. **Regular Updates**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade

   # Update Docker images
   docker-compose pull
   docker-compose --profile production up -d
   ```

3. **Backup Strategy**
   - Regular server backups
   - SSL certificate backups
   - Application code in version control

## Troubleshooting

### Common Issues

1. **SSL Certificate Issues**
   ```bash
   # Check certificate validity
   openssl x509 -in ssl/cert.pem -text -noout
   
   # Test SSL connection
   openssl s_client -connect api.mypisang.info:443
   ```

2. **Service Not Starting**
   ```bash
   # Check container status
   docker-compose ps
   
   # View error logs
   docker-compose logs attendance-api
   ```

3. **DNS Issues**
   ```bash
   # Verify DNS resolution
   nslookup api.mypisang.info
   dig api.mypisang.info
   ```

## Support

For issues with the deployment, check:
1. Container logs: `docker-compose logs`
2. Nginx error logs: `docker-compose logs nginx`
3. Application logs: `docker-compose logs attendance-api`