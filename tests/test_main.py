import asyncio
import pytest
from main import parse_time, format_time_minimal


class TestParseTime:
    @pytest.mark.asyncio
    async def test_empty_returns_default(self):
        assert await parse_time(None) == 60
        assert await parse_time("") == 60
        assert await parse_time("   ") == 60

    @pytest.mark.asyncio
    async def test_seconds_only(self):
        assert await parse_time("30s") == 30
        assert await parse_time("1s") == 1
        assert await parse_time("0s") == 60  # no match or zero -> default

    @pytest.mark.asyncio
    async def test_minutes_only(self):
        assert await parse_time("5m") == 300
        assert await parse_time("1m") == 60
        assert await parse_time("10m") == 600

    @pytest.mark.asyncio
    async def test_hours_only(self):
        assert await parse_time("1h") == 3600
        assert await parse_time("2h") == 7200

    @pytest.mark.asyncio
    async def test_combined(self):
        assert await parse_time("1h30m") == 3600 + 1800
        assert await parse_time("1h30m15s") == 3600 + 1800 + 15
        assert await parse_time("2h5m") == 7200 + 300

    @pytest.mark.asyncio
    async def test_minimum_one_second(self):
        assert await parse_time("0h0m1s") == 1


class TestFormatTimeMinimal:
    def test_under_one_minute(self):
        assert format_time_minimal(0) == "0:00"
        assert format_time_minimal(45) == "0:45"
        assert format_time_minimal(59) == "0:59"

    def test_minutes_only(self):
        assert format_time_minimal(60) == "1:00"
        assert format_time_minimal(90) == "1:30"
        assert format_time_minimal(599) == "9:59"

    def test_hours(self):
        assert format_time_minimal(3600) == "1:00:00"
        assert format_time_minimal(3661) == "1:01:01"
        assert format_time_minimal(7325) == "2:02:05"

    def test_negative_clamped_to_zero(self):
        assert format_time_minimal(-1) == "0:00"

    def test_float_seconds(self):
        assert format_time_minimal(65.7) == "1:05"
