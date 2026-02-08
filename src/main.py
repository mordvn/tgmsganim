import asyncio
import re
from datetime import datetime, timedelta
from aiogram import Router, Bot, Dispatcher, F, types
import logging
import random
import os
from dotenv import load_dotenv

load_dotenv()

router = Router(name=__name__)
lock = asyncio.Lock()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FBI_BANNER = [
    "🌎\n\n     FBI\nTHIS SITE HAS BEEN SEIZED",
    "🌍\n\n     FBI\nTHIS SITE HAS BEEN SEIZED",
    "🌏\n\n     FBI\nTHIS SITE HAS BEEN SEIZED",
]

MIN_RESPONSE_TIME = 3
TYPING_SPEED = 0.1


async def animate_message(message: types.Message, frames, iterations=3, interval=0.5):
    msg = await message.answer(frames[0])

    last_frame = frames[0]
    for _ in range(iterations):
        for frame in frames:
            if frame == last_frame:
                continue

            await asyncio.sleep(interval)
            try:
                await msg.edit_text(frame)
                last_frame = frame
            except Exception as e:
                logger.error(f"Error updating animation: {e}")

    return msg


async def type_text_animation(message: types.Message, text: str):
    msg = await message.answer("▌")
    current_text = ""

    for char in text:
        current_text += char
        try:
            await msg.edit_text(current_text + "▌")
            await asyncio.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            logger.error(f"Error in type animation: {e}")

    await msg.edit_text(current_text)
    return msg


async def parse_time(time_str):
    if not time_str:
        return 60

    total_seconds = 0

    hour_match = re.search(r"(\d+)h", time_str)
    minute_match = re.search(r"(\d+)m", time_str)
    second_match = re.search(r"(\d+)s", time_str)

    if hour_match:
        total_seconds += int(hour_match.group(1)) * 3600
    if minute_match:
        total_seconds += int(minute_match.group(1)) * 60
    if second_match:
        total_seconds += int(second_match.group(1))

    return max(1, total_seconds)


async def ad_scroll_animation(
    message: types.Message, ad_text: str, duration_str: str, width_str=None
):
    duration_seconds = await parse_time(duration_str)
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)

    display_width = 30
    if width_str:
        match = re.match(r"(\d+)ch", width_str)
        if match:
            display_width = int(match.group(1))
            display_width = max(10, min(50, display_width))

    msg = await message.answer("│" + " " * display_width + "│")

    padded_text = " " * display_width + ad_text + " " * display_width

    position = 0

    while datetime.now() < end_time:
        visible_text = padded_text[position : position + display_width]

        ad_display = f"│{visible_text}│"

        try:
            await msg.edit_text(ad_display)
        except Exception as e:
            logger.error(f"Error updating ad scroll: {e}")

        position = (position + 1) % (len(padded_text) - display_width)

        await asyncio.sleep(0.3)

    try:
        await msg.edit_text(f"│{ad_text.center(display_width)}│")
    except Exception as e:
        logger.error(f"Error updating final ad: {e}")

    return msg


async def timer_animation(message: types.Message, duration_str: str, timer_text=None):
    duration_seconds = await parse_time(duration_str)

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)

    if not timer_text:
        timer_text = "Timer"

    msg = await message.answer("⏳ Starting...")

    while datetime.now() < end_time:
        now = datetime.now()
        elapsed = (now - start_time).total_seconds()
        remaining = duration_seconds - elapsed

        progress_pct = min(100, (elapsed / duration_seconds) * 100)
        progress_bar_length = 12
        filled_length = int(progress_bar_length * progress_pct / 100)

        bar = "█" * filled_length + "▒" * (progress_bar_length - filled_length)

        elapsed_str = format_time_minimal(elapsed)
        remaining_str = format_time_minimal(remaining)

        timer_display = f"{timer_text}\n{elapsed_str} {bar} {remaining_str}"

        try:
            await msg.edit_text(timer_display)
        except Exception as e:
            logger.error(f"Error updating timer: {e}")

        update_interval = min(5, max(1, int(duration_seconds / 100)))
        await asyncio.sleep(update_interval)

    try:
        await msg.edit_text(f"{timer_text} ✓")
    except Exception as e:
        logger.error(f"Error updating final timer: {e}")

    return msg


def format_time_minimal(seconds):
    seconds = int(seconds)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:01d}:{seconds:02d}"


ASCII_GLOBE = [
    "    .--.    \n   /    \   \n  |      |  \n   \\    /   \n    '--'    ",
    "    .--.    \n   /    \\   \n  (      )  \n   \\    /   \n    '--'    ",
    "    .--.    \n   /    \\   \n  |      |  \n   \\    /   \n    '--'    ",
    "    .--.    \n   /    \\   \n  (      )  \n   \\    /   \n    '--'    ",
]


async def fbi_banner_animation(message: types.Message, duration_str=None):
    duration_seconds = 30
    if duration_str:
        duration_seconds = await parse_time(duration_str)

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)

    fbi_seizure_template = """{}

FEDERAL BUREAU OF INVESTIGATION

THIS ACCOUNT HAS BEEN SEIZED

as part of an enforcement action by the
Federal Bureau of Investigation"""

    msg = await message.answer("...")

    for _ in range(3):
        try:
            await msg.edit_text("⚠️")
            await asyncio.sleep(0.3)
            await msg.edit_text("")
            await asyncio.sleep(0.2)
        except Exception as e:
            logger.error(f"Error in FBI animation: {e}")

    globe_emojis = ["🌎", "🌍", "🌏"]
    globe_index = 0

    while datetime.now() < end_time:
        globe = globe_emojis[globe_index]
        try:
            current_text = fbi_seizure_template.format(globe)
            await msg.edit_text(current_text)
            globe_index = (globe_index + 1) % len(globe_emojis)
            await asyncio.sleep(0.4)
        except Exception as e:
            logger.error(f"Error in FBI globe animation: {e}")

    final_banner = fbi_seizure_template.format("🌎")
    try:
        await msg.edit_text(final_banner)
    except Exception as e:
        logger.error(f"Error setting final FBI banner: {e}")

    return msg


@router.business_message(
    lambda message: message.text and message.text.startswith(".type ")
)
async def handle_type_command(message: types.Message):
    text = message.text[6:].strip()
    if not text:
        await message.answer("Please provide text to type. Example: .type Hello world")
        return

    asyncio.create_task(type_text_animation(message, text))


@router.business_message(
    lambda message: message.text and message.text.startswith(".timer ")
)
async def handle_timer_command(message: types.Message):
    parts = message.text[7:].strip().split('"')

    if len(parts) >= 3 and parts[1].strip():
        timer_text = parts[1].strip()
        duration = parts[2].strip()
    else:
        timer_text = None
        duration = message.text[7:].strip()

    if not duration:
        await message.answer(
            'Please provide a duration. Example: .timer 30m or .timer "Meeting" 30m'
        )
        return

    asyncio.create_task(timer_animation(message, duration, timer_text))


@router.business_message(
    lambda message: message.text and message.text.startswith(".fbi")
)
async def handle_fbi_command(message: types.Message):
    text = message.text.strip()
    duration_str = None

    if len(text) > 4:
        duration_str = text[4:].strip()

    asyncio.create_task(fbi_banner_animation(message, duration_str))


@router.business_message(
    lambda message: message.text and message.text.startswith(".ad ")
)
async def handle_ad_command(message: types.Message):
    parts = message.text[4:].strip().split()

    if len(parts) < 2:
        await message.answer(
            'Please provide ad text and duration. Example: .ad "Selling something" 10m 20ch'
        )
        return

    width_str = None
    if len(parts) >= 3 and "ch" in parts[-1]:
        width_str = parts.pop()

    duration = parts.pop()

    ad_text = " ".join(parts)
    ad_text = ad_text.strip("\"'")

    asyncio.create_task(ad_scroll_animation(message, ad_text, duration, width_str))


async def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("No BOT_TOKEN found in .env file")
        return

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
