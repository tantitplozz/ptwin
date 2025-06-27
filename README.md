# 🔥 GOD-TIER PhantomAutoBuyBot - Complete Full Stack Solution

> **The Ultimate iPhone Purchase Automation System with Advanced AI, Stealth Technology, and Real-time Monitoring**

## 🌟 Features Overview

### 🧠 **Core Intelligence**
- **Advanced Memory System** - VectorDB-like learning and optimization
- **A/B Testing Engine** - Multi-profile performance optimization
- **Dynamic Agent Behavior** - Adaptive strategies based on success patterns
- **Pattern Recognition** - Smart detection and response systems

### 🛡️ **Stealth Technology**
- **GoLogin Integration** - Professional browser fingerprinting
- **Human Behavior Simulation** - Natural mouse movements, typing, scrolling
- **Anti-Detection Systems** - Advanced evasion techniques
- **Warmup Agent** - Realistic browsing patterns before purchase

### 💳 **Payment Intelligence**
- **Smart Payment Detection** - Automatic method identification
- **Pattern-Based Selection** - Historical success rate optimization
- **Multiple Payment Support** - Credit Card, Apple Pay, PromptPay, Bank Transfer
- **OTP Automation** - Advanced verification handling

### 📊 **Real-time Monitoring**
- **WebSocket Dashboard** - Live status and control interface
- **Telegram Notifications** - Rich formatted real-time updates
- **Performance Analytics** - Detailed metrics and insights
- **Error Recovery** - Intelligent failure handling

## 🚀 Quick Start

### 1. **Clone & Setup**
```bash
git clone https://github.com/tantitplozz/ptwin.git
cd ptwin
cp .env.template .env
# Edit .env with your credentials
```

### 2. **Deploy with Docker**
```bash
# Build and run
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f phantom-autobuy
```

### 3. **Monitor & Control**
- **WebSocket Dashboard**: http://localhost:8686
- **Telegram Notifications**: Real-time updates
- **Live Logs**: `docker-compose logs -f`

## 📦 Complete Module Architecture

### 🔥 **Core Modules**

#### `main.py` - **GOD-TIER Orchestrator**
- Complete flow coordination
- Error handling and recovery
- Performance monitoring
- Resource management

#### `browser_stealth.py` - **Stealth Browser Engine**
- GoLogin integration
- Anti-detection mechanisms
- Fallback browser support
- Human behavior simulation

#### `warmup_agent.py` - **Human-like Warmup**
- Natural browsing patterns
- Multi-phase preparation
- Behavioral learning
- Stealth optimization

#### `memory.py` - **VectorDB Memory System**
- Session data persistence
- Pattern recognition
- Success rate tracking
- Optimization recommendations

#### `purchase_flow.py` - **Purchase Automation**
- 8-step purchase process
- Intelligent product selection
- Error recovery mechanisms
- Screenshot documentation

#### `payment_patterns.py` - **Payment Intelligence**
- Smart method detection
- Historical optimization
- Multi-payment support
- Risk assessment

#### `otp.py` - **OTP Automation**
- Multi-method OTP handling
- API integration support
- Fallback mechanisms
- Success verification

#### `monitor_ws.py` - **Real-time Monitoring**
- WebSocket server
- Live dashboard
- Control commands
- Performance metrics

#### `telegram_notify.py` - **Rich Notifications**
- Formatted messages
- Photo/document support
- Queue management
- Rate limiting

#### `ab_tester.py` - **A/B Testing Engine**
- Multi-profile testing
- Performance analysis
- Optimization recommendations
- Historical learning

#### `config.py` - **Configuration Management**
- Environment variables
- Default settings
- Validation
- Type safety

## 🎯 Target Configuration

### **Default Target**
- **Product**: iPhone 16 Pro Max
- **Storage**: 1TB
- **Color**: Natural Titanium
- **Carrier**: Unlocked

### **Customization**
Edit `.env` file or modify `config.py` for different targets.

## 📊 Monitoring & Analytics

### **WebSocket Dashboard** (Port 8686)
```javascript
// Real-time status updates
{
  "bot_status": "running",
  "current_step": "purchase_execution",
  "progress": 75,
  "session_id": "AB_12345678"
}
```

### **Telegram Notifications**
- 🔥 Startup notifications
- 📊 Step-by-step progress
- 💳 Payment processing updates
- 🔐 OTP handling status
- ✅ Success confirmations
- ❌ Error alerts

### **Performance Metrics**
- Success rates by profile
- Average execution times
- Detection event tracking
- Optimization recommendations

## 🧪 A/B Testing System

### **Test Profiles**
1. **Conservative** - Maximum stealth, slower execution
2. **Balanced** - Optimal speed/stealth balance
3. **Aggressive** - Faster execution, higher risk
4. **Historical** - Based on past success patterns

### **Metrics Tracked**
- Success rate
- Execution time
- Detection events
- Error rates
- Overall performance score

## 🛡️ Security Features

### **Stealth Mechanisms**
- Browser fingerprint randomization
- Human-like timing patterns
- Natural mouse movements
- Realistic typing speeds
- Anti-automation detection

### **Data Protection**
- Environment variable encryption
- Secure credential handling
- Session data isolation
- Clean resource cleanup

## 🔧 Configuration Options

### **Environment Variables**
```env
# Core Configuration
GOLOGIN_API_KEY=your-api-key
TELEGRAM_TOKEN=your-bot-token
TARGET_PRODUCT=iPhone 16 Pro Max

# Performance Tuning
AB_TEST_PROFILES=3
STEALTH_MODE=true
HUMAN_DELAY_MIN=1000

# Monitoring
MONITOR_PORT=8686
TELEGRAM_NOTIFICATIONS=true
```

## 🐳 Docker Deployment

### **Single Container**
```bash
docker build -t ptwin:latest .
docker run --env-file .env -p 8686:8686 ptwin:latest
```

### **Full Stack with Docker Compose**
```bash
# Basic deployment
docker-compose up -d

# Advanced with Redis/PostgreSQL
docker-compose --profile advanced up -d
```

## 📈 Performance Optimization

### **Memory Management**
- Efficient session storage
- Automatic cleanup
- Resource monitoring
- Memory leak prevention

### **Speed Optimization**
- Parallel processing where safe
- Intelligent caching
- Optimized selectors
- Reduced wait times

### **Reliability**
- Multiple retry mechanisms
- Fallback strategies
- Error recovery
- Health monitoring

## 🔍 Troubleshooting

### **Common Issues**

#### **GoLogin Connection Failed**
```bash
# Check API key and profile ID
# Verify GoLogin credits
# Test with fallback browser
```

#### **Payment Processing Errors**
```bash
# Verify payment method availability
# Check form field selectors
# Review error logs
```

#### **OTP Handling Issues**
```bash
# Confirm OTP service configuration
# Check API integration
# Verify phone number format
```

### **Debug Mode**
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SCREENSHOT_ON_ERROR=true
```

## 🚀 Advanced Usage

### **AllHands Integration**
```yaml
# Import .allhands.yaml
# Configure workflow parameters
# Execute via AllHands interface
```

### **Custom Profiles**
```python
# Modify ab_tester.py
# Add custom behavioral patterns
# Implement specific timing strategies
```

### **API Extensions**
```python
# Extend monitor_ws.py
# Add custom endpoints
# Implement additional controls
```

## 📊 Success Metrics

### **Key Performance Indicators**
- **Success Rate**: Target >90%
- **Execution Time**: <5 minutes average
- **Detection Rate**: <5%
- **Error Recovery**: >95%

### **Optimization Goals**
- Minimize detection events
- Maximize purchase success
- Optimize execution speed
- Improve stealth effectiveness

## ⚠️ Legal & Ethical Considerations

### **Important Disclaimers**
- **Educational Purpose Only**
- **Comply with Website Terms of Service**
- **Respect Rate Limits**
- **Use Responsibly**

### **Best Practices**
- Test in development environments
- Respect website policies
- Monitor for detection
- Use appropriate delays

## 🤝 Support & Community

### **Documentation**
- Complete API documentation
- Video tutorials
- Best practices guide
- Troubleshooting manual

### **Community**
- GitHub Issues for bug reports
- Discord for real-time support
- Telegram for updates

---

## 🎉 **Ready to Deploy!**

Your GOD-TIER PhantomAutoBuyBot is ready for deployment with all advanced features:

✅ **Complete Full Stack Architecture**  
✅ **Advanced AI & Memory Systems**  
✅ **Real-time Monitoring & Control**  
✅ **Professional Stealth Technology**  
✅ **Intelligent Payment Processing**  
✅ **A/B Testing & Optimization**  
✅ **Docker & AllHands Integration**  

**Deploy now and experience the ultimate in automated iPhone purchasing!** 🔥🤖

---

*Built with ❤️ for the ultimate automation experience*