# TradingView Data API

Real-time market data API powered by TradingView with WebSocket support.

## Deployment Instructions for Hostinger VPS

### Prerequisites

1. A Hostinger VPS with Ubuntu/Debian
2. Python 3.12 installed
3. Domain name pointed to your VPS IP
4. SSH access to your VPS

### Step-by-Step Deployment

1. **Connect to your VPS**
   ```bash
   ssh username@your_vps_ip
   ```

2. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

3. **Update configuration files**
   - Edit `tvdata.service`: Replace `your_username` with your VPS username
   - Edit `tvdata.conf`: Replace `your_domain.com` with your actual domain
   - Edit `.env`: Update environment variables as needed
   - Edit `tvdata.supervisor.conf`: Replace `your_username` with your VPS username

4. **Make deploy script executable**
   ```bash
   chmod +x deploy.sh
   ```

5. **Run deployment script**
   ```bash
   ./deploy.sh
   ```

### Manual Deployment Steps (if needed)

1. **Create application directory**
   ```bash
   sudo mkdir -p /var/www/tvdata-api
   sudo chown -R $USER:$USER /var/www/tvdata-api
   ```

2. **Set up Python virtual environment**
   ```bash
   python3.12 -m venv /var/www/tvdata-api/venv
   source /var/www/tvdata-api/venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Nginx**
   ```bash
   sudo cp tvdata.conf /etc/nginx/sites-available/tvdata
   sudo ln -s /etc/nginx/sites-available/tvdata /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Set up systemd service**
   ```bash
   sudo cp tvdata.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable tvdata
   sudo systemctl start tvdata
   ```

6. **Set up SSL (optional)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```

### Monitoring and Maintenance

1. **Check service status**
   ```bash
   sudo systemctl status tvdata
   ```

2. **View logs**
   ```bash
   # Service logs
   sudo journalctl -u tvdata
   
   # Nginx logs
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Restart service**
   ```bash
   sudo systemctl restart tvdata
   ```

### API Documentation

After deployment, API documentation will be available at:
- Swagger UI: `https://your_domain.com/docs`
- ReDoc: `https://your_domain.com/redoc`

### WebSocket Endpoints

- WebSocket URL: `wss://your_domain.com/ws/{client_id}`
- Subscribe format:
  ```json
  {
    "action": "subscribe",
    "symbol": "NIFTY",
    "exchange": "NSE",
    "interval": "1m"
  }
  ```

### Security Notes

1. Always use HTTPS in production
2. Keep your TradingView token secure
3. Update the CORS settings in production
4. Regularly update dependencies
5. Monitor system resources

### Troubleshooting

1. **Service won't start**
   - Check logs: `sudo journalctl -u tvdata -n 50`
   - Verify Python path: `which python3.12`
   - Check permissions: `ls -la /var/www/tvdata-api`

2. **WebSocket connection issues**
   - Verify Nginx configuration
   - Check SSL certificate
   - Ensure ports are open

3. **Data not updating**
   - Check TradingView token validity
   - Verify internet connectivity
   - Check rate limits

For additional support, please open an issue on the repository. 