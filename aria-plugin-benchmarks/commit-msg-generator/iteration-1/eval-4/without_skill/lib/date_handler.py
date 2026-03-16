"""
Unified Date Handling Module

This module consolidates date formatting, timezone handling,
and date conversion utilities into a single, coherent interface.
"""

from datetime import datetime
from typing import Optional, List
import pytz


class DateHandler:
    """
    Unified date and timezone handler.

    Provides consistent methods for:
    - Date formatting and parsing
    - Timezone conversions
    - Date calculations
    """

    # Common format presets
    ISO_DATE = "%Y-%m-%d"
    ISO_DATETIME = "%Y-%m-%dT%H:%M:%S"
    ISO_DATETIME_TZ = "%Y-%m-%dT%H:%M:%S%z"
    READABLE = "%B %d, %Y at %I:%M %p"
    READABLE_TZ = "%B %d, %Y at %I:%M %p %Z"

    def __init__(self, default_tz: str = "UTC", default_format: str = ISO_DATE):
        """
        Initialize DateHandler.

        Args:
            default_tz: Default timezone name (e.g., 'UTC', 'America/New_York')
            default_format: Default date format string
        """
        self.default_tz = default_tz
        self.default_format = default_format

    # ========== Timezone Methods ==========

    def get_timezone(self, tz_name: str) -> pytz.BaseTzInfo:
        """Get timezone object by name."""
        return pytz.timezone(tz_name)

    def localize(self, dt: datetime, tz_name: Optional[str] = None) -> datetime:
        """Localize naive datetime to timezone."""
        tz = self.get_timezone(tz_name or self.default_tz)
        return tz.localize(dt)

    def convert_timezone(self, dt: datetime, to_tz: str) -> datetime:
        """Convert datetime to target timezone."""
        tz = self.get_timezone(to_tz)
        return dt.astimezone(tz)

    def is_dst(self, dt: datetime, tz_name: Optional[str] = None) -> bool:
        """Check if datetime is in daylight saving time."""
        tz = self.get_timezone(tz_name or self.default_tz)
        return tz.localize(dt).dst() != datetime.timedelta(0)

    # ========== Formatting Methods ==========

    def format(self, dt: datetime, format_str: Optional[str] = None) -> str:
        """Format datetime with specified format."""
        fmt = format_str or self.default_format
        return dt.strftime(fmt)

    def format_iso(self, dt: datetime) -> str:
        """Format as ISO 8601 string."""
        return dt.strftime(self.ISO_DATETIME)

    def format_iso_tz(self, dt: datetime) -> str:
        """Format as ISO 8601 with timezone."""
        return dt.strftime(self.ISO_DATETIME_TZ)

    def format_readable(self, dt: datetime, with_tz: bool = False) -> str:
        """Format in human-readable format."""
        fmt = self.READABLE_TZ if with_tz else self.READABLE
        return dt.strftime(fmt)

    def format_with_timezone(self, dt: datetime, tz: str, format_str: Optional[str] = None) -> str:
        """Format datetime with timezone information."""
        timezone = pytz.timezone(tz)
        dt_aware = timezone.localize(dt) if dt.tzinfo is None else dt.astimezone(timezone)
        fmt = format_str or self.READABLE_TZ
        return dt_aware.strftime(fmt)

    # ========== Parsing Methods ==========

    def parse(self, date_str: str, format_str: Optional[str] = None) -> datetime:
        """Parse date string to datetime."""
        fmt = format_str or self.default_format
        return datetime.strptime(date_str, fmt)

    def parse_with_timezone(self, date_str: str, tz: str, format_str: Optional[str] = None) -> datetime:
        """Parse string to datetime and apply timezone."""
        fmt = format_str or self.ISO_DATETIME.replace("T", " ")
        dt = datetime.strptime(date_str, fmt)
        timezone = pytz.timezone(tz)
        return timezone.localize(dt)

    # ========== Utility Methods ==========

    def now(self, tz_name: Optional[str] = None) -> datetime:
        """Get current time in timezone."""
        tz = self.get_timezone(tz_name or self.default_tz)
        return datetime.now(tz)

    def format_range(self, start: datetime, end: datetime, format_str: Optional[str] = None) -> str:
        """Format a date range."""
        fmt = format_str or self.default_format
        return f"{start.strftime(fmt)} - {end.strftime(fmt)}"

    def format_list(self, dates: List[datetime], format_str: Optional[str] = None) -> List[str]:
        """Format list of dates."""
        fmt = format_str or self.default_format
        return [d.strftime(fmt) for d in dates]


# Convenience functions for quick operations
def quick_format(dt: datetime) -> str:
    """Quick format date in standard format."""
    return dt.strftime("%Y-%m-%d")


def quick_format_with_time(dt: datetime) -> str:
    """Quick format date with time."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_time(tz: Optional[str] = None) -> datetime:
    """Get current time, optionally in specific timezone."""
    if tz:
        timezone = pytz.timezone(tz)
        return datetime.now(timezone)
    return datetime.now()
