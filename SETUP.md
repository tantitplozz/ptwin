# 🔥 GOD-TIER PhantomAutoBuyBot - Setup Guide

## 🚀 Quick Start (5 Minutes)

### 1. **Clone Repository**
```bash
git clone https://github.com/tantitplozz/ptwin.git
cd ptwin
```

### 2. **Easy Setup Script**
```bash
python run.py
```
The script will guide you through:
- ✅ Requirements checking
- 📦 Dependency installation  
- 📝 Configuration setup
- 🚀 Deployment options

### 3. **Configure Credentials**
Edit `.env` file with your credentials:
```env
# Required
GOLOGIN_API_KEY=your-gologin-api-key
GOLOGIN_PROFILE_ID=your-profile-id
TELEGRAM_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Optional (for testing)
PAYMENT_CARD_NUMBER=4111111111111111
PAYMENT_EXP=12/29
PAYMENT_CVV=123
```

### 4. **Deploy & Run**
Choose your preferred method:

#### **Option A: Docker (Recommended)**
```bash
docker-compose up -d
```

#### **Option B: Local Python**
```bash
python run.py
# Select option 1
```

### 5. **Monitor & Control**
- **Dashboard**: http://localhost:8686
- **Telegram**: Real-time notifications
- **Logs**: `docker-compose logs -f`

---

## 📋 Detailed Setup

### **Prerequisites**
- Python 3.10+
- Docker & Docker Compose (optional)
- GoLogin account with API access
- Telegram bot token

### **GoLogin Setup**
1. Sign up at [GoLogin.com](https://gologin.com)
2. Create browser profile
3. Get API key from dashboard
4. Note your profile ID

### **Telegram Setup**
1. Create bot via [@BotFather](https://t.me/botfather)
2. Get bot token
3. Get your chat ID from [@userinfobot](https://t.me/userinfobot)

### **Environment Configuration**
```env
# Core Configuration
GOLOGIN_API_KEY=gl_live_xxxxxxxxxxxxxxxx
GOLOGIN_PROFILE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Target Configuration
TARGET_PRODUCT=iPhone 16 Pro Max
TARGET_STORAGE=1TB
TARGET_COLOR=Natural Titanium
TARGET_CARRIER=Unlocked

# Performance Tuning
STEALTH_MODE=true
AB_TEST_PROFILES=3
HUMAN_DELAY_MIN=1000
HUMAN_DELAY_MAX=5000

# Monitoring
MONITOR_PORT=8686
MONITOR_HOST=0.0.0.0
```

---

## 🐳 Docker Deployment

### **Basic Deployment**
```bash
# Build and run
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f phantom-autobuy

# Stop
docker-compose down
```

### **Advanced Deployment (with Redis/PostgreSQL)**
```bash
# Run with advanced features
docker-compose --profile advanced up -d

# Includes:
# - Redis for caching
# - PostgreSQL for analytics
# - Enhanced monitoring
```

### **Custom Docker Build**
```bash
# Build custom image
docker build -t ptwin:custom .

# Run with custom settings
docker run --env-file .env -p 8686:8686 ptwin:custom
```

---

## 🔧 Local Development

### **Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### **Run Components Separately**

#### **Monitor Only**
```bash
python phantom_autobuy/monitor_ws.py
```

#### **Test Configuration**
```bash
python -c "from phantom_autobuy import config; print('Config loaded successfully')"
```

#### **Test Telegram**
```bash
python -c "
from phantom_autobuy.telegram_notify import send_telegram
import asyncio
asyncio.run(send_telegram('Test message'))
"
```

---

## 📊 Monitoring & Control

### **WebSocket Dashboard**
Access at: http://localhost:8686

Features:
- Real-time status updates
- Live progress tracking
- Control commands (pause/resume/stop)
- Performance metrics
- Error monitoring

### **Telegram Notifications**
Rich formatted messages for:
- 🔥 Bot startup/shutdown
- 📊 Step-by-step progress
- 💳 Payment processing
- 🔐 OTP handling
- ✅ Success confirmations
- ❌ Error alerts

### **Log Monitoring**
```bash
# Docker logs
docker-compose logs -f phantom-autobuy

# Local logs
tail -f phantom_bot.log
```

---

## 🧪 Testing & Validation

### **Configuration Test**
```bash
python run.py
# Select option 4: Test Configuration
```

### **Stealth Test**
```bash
# Test browser stealth
python -c "
from phantom_autobuy.browser_stealth import launch_stealth_browser
import asyncio
asyncio.run(launch_stealth_browser())
"
```

### **Memory System Test**
```bash
# Test memory system
python -c "
from phantom_autobuy.memory import MemoryManager
memory = MemoryManager()
print('Memory system working')
"
```

---

## ⚡ Performance Optimization

### **Speed Optimization**
```env
# Faster execution (higher risk)
STEALTH_MODE=false
HUMAN_DELAY_MIN=500
HUMAN_DELAY_MAX=2000
AB_TEST_PROFILES=1
```

### **Maximum Stealth**
```env
# Slower but safer
STEALTH_MODE=true
HUMAN_DELAY_MIN=2000
HUMAN_DELAY_MAX=8000
AB_TEST_PROFILES=3
```

### **Balanced Performance**
```env
# Recommended settings
STEALTH_MODE=true
HUMAN_DELAY_MIN=1000
HUMAN_DELAY_MAX=5000
AB_TEST_PROFILES=2
```

---

## 🔍 Troubleshooting

### **Common Issues**

#### **GoLogin Connection Failed**
```bash
# Check API key
echo $GOLOGIN_API_KEY

# Test connection
curl -H "Authorization: Bearer $GOLOGIN_API_KEY" \
     https://api.gologin.com/browser/profiles
```

#### **Telegram Not Working**
```bash
# Test bot token
curl "https://api.telegram.org/bot$TELEGRAM_TOKEN/getMe"

# Test chat ID
curl "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
     -d "chat_id=$TELEGRAM_CHAT_ID&text=Test"
```

#### **Docker Issues**
```bash
# Check Docker
docker --version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### **Permission Issues**
```bash
# Fix permissions
chmod +x run.py
sudo chown -R $USER:$USER .
```

### **Debug Mode**
```env
# Enable debug logging
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SCREENSHOT_ON_ERROR=true
```

### **Health Checks**
```bash
# Check container health
docker-compose ps

# Check WebSocket
curl http://localhost:8686

# Check logs for errors
docker-compose logs phantom-autobuy | grep ERROR
```

---

## 🔐 Security Best Practices

### **Credential Security**
- Never commit `.env` file
- Use strong API keys
- Rotate credentials regularly
- Use environment-specific configs

### **Network Security**
- Use VPN when possible
- Configure firewall rules
- Monitor for detection events
- Use proxy rotation

### **Operational Security**
- Test in development first
- Monitor success rates
- Respect rate limits
- Follow website terms of service

---

## 📈 Advanced Configuration

### **Custom Profiles**
Edit `phantom_autobuy/ab_tester.py` to add custom behavioral profiles:
```python
# Add custom profile
custom_profile = {
    'name': 'Custom',
    'characteristics': {
        'speed': 'medium',
        'stealth_level': 'maximum',
        'delay_multiplier': 1.5
    }
}
```

### **Payment Methods**
Configure payment preferences in `phantom_autobuy/payment_patterns.py`:
```python
# Modify payment method priorities
payment_methods = {
    'apple_pay': {'priority': 1},
    'credit_card': {'priority': 2},
    'promptpay': {'priority': 3}
}
```

### **Target Customization**
Modify target product in `.env`:
```env
TARGET_PRODUCT=iPhone 15 Pro
TARGET_STORAGE=512GB
TARGET_COLOR=Blue Titanium
```

---

## 🎯 Success Optimization

### **Key Metrics to Monitor**
- Success rate >90%
- Average execution time <5 minutes
- Detection events <5%
- Error recovery rate >95%

### **Optimization Tips**
1. **Use A/B Testing** - Let the system find optimal settings
2. **Monitor Detection** - Adjust stealth if detection increases
3. **Analyze Patterns** - Review memory data for insights
4. **Update Regularly** - Keep selectors and methods current

### **Best Practices**
- Start with conservative settings
- Gradually optimize based on results
- Monitor for website changes
- Maintain multiple profiles

---

## 🆘 Support

### **Getting Help**
- 📖 Check documentation first
- 🐛 Search existing GitHub issues
- 💬 Join community Discord
- 📧 Contact support team

### **Reporting Issues**
Include:
- Error messages
- Configuration (without credentials)
- Steps to reproduce
- System information

---

## ✅ Ready to Deploy!

Your GOD-TIER PhantomAutoBuyBot is now ready for deployment. Follow this checklist:

- [ ] ✅ Repository cloned
- [ ] 📝 Configuration completed
- [ ] 🔑 Credentials configured
- [ ] 🧪 Configuration tested
- [ ] 🚀 Deployment method chosen
- [ ] 📊 Monitoring dashboard accessible
- [ ] 📱 Telegram notifications working

**Deploy now and experience the ultimate in automated iPhone purchasing!** 🔥🤖