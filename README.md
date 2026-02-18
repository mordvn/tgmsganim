# TG Message Animator

A Telegram bot that creates interactive animated messages with various effects like typing animations, timers, scrolling ads, and FBI seizure notices.

<div align="center">
<img src="images/example.png" alt="Demo image" width="300">
</div>

## Features

- **Typing Animation**: Simulates real-time typing with a blinking cursor
- **Timer**: Creates a visual countdown timer with progress bar
- **Scrolling Ad**: Displays text that scrolls horizontally
- **FBI Seizure Banner**: Shows an animated FBI seizure notice with rotating globe

## Setup

### Prerequisites

- Python 3
- Telegram Premium account
- Bot with Business mode enabled

### Installation

1. Clone this repository:
```bash
git clone https://github.com/mordvn/tgmessageanimator.git
cd tgmessageanimator
```

2. Install dependencies:
```bash
uv sync
 ```

3. Create a .env file in the project root:
```plaintext
BOT_TOKEN=your_bot_token_here
 ```

### Telegram Bot Setup
1. Purchase Telegram Premium if you don't already have it
2. Create a bot through @BotFather
3. Enable Business mode for your bot:
   - Send /mybots to BotFather
   - Select your bot
   - Choose "Bot Settings" > "Business Settings" > "Enable Business Features"
4. Connect your bot to your Telegram profile:
   - Go to your Telegram settings
   - Select "Business Tools" > "Connected Bot"
   - Choose your bot from the list
   - Select which chats the bot can access (or leave as is to allow it to respond to anyone)

## Usage
Start the bot:

```bash
uv run python3 src/main.py
 ```

### Available Commands
- Typing Animation : .type Your text here
  
  - Simulates typing the text character by character
- Timer : .timer 5m or .timer "Meeting" 1h 30m
  
  - Creates a countdown timer with optional label
  - Supports time formats: hours (h), minutes (m), seconds (s)
  - Examples: 30m , 1h 30m , 2h 45m 30s
- Scrolling Ad : .ad Your ad text here 30s 20ch
  
  - Creates a horizontally scrolling text banner
  - Last parameter is duration (required)
  - Optional width parameter (e.g., 20ch for 20 characters)
- FBI Seizure Notice : .fbi or .fbi 1m
  
  - Displays an animated FBI seizure notice
  - Optional duration parameter (default: 30 seconds)
  
### Examples
- .type Hello, I'm typing this message in real-time!
- .timer "Coffee Break" 15m
- .ad Special offer today only! 1m 30ch
- .fbi 2m

## License

[MIT](https://choosealicense.com/licenses/mit/)
