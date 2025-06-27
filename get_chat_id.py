#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Get Telegram Chat ID
Get updates to find your chat ID
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def get_chat_id():
    """Get chat ID from Telegram updates"""
    
    if not TELEGRAM_TOKEN:
        print("❌ [TELEGRAM] Missing token")
        return
    
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/getUpdates") as response:
                if response.status == 200:
                    data = await response.json()
                    if data['ok']:
                        updates = data['result']
                        if updates:
                            print("📊 [TELEGRAM] Recent messages:")
                            for update in updates[-5:]:  # Show last 5 updates
                                if 'message' in update:
                                    msg = update['message']
                                    chat = msg['chat']
                                    user = msg.get('from', {})
                                    print(f"💬 Chat ID: {chat['id']}")
                                    print(f"👤 User: {user.get('first_name', 'N/A')} (@{user.get('username', 'N/A')})")
                                    print(f"📝 Text: {msg.get('text', 'N/A')}")
                                    print("---")
                        else:
                            print("ℹ️ [TELEGRAM] No messages found. Send a message to @AI_IM_WIN_BOT first!")
                    else:
                        print(f"❌ [TELEGRAM] API error: {data}")
                else:
                    print(f"❌ [TELEGRAM] HTTP Error: {response.status}")
        except Exception as e:
            print(f"❌ [TELEGRAM] Failed: {e}")

if __name__ == "__main__":
    print("🔍 Getting Telegram Chat ID...")
    print("📱 Send a message to @AI_IM_WIN_BOT first, then run this script")
    asyncio.run(get_chat_id())