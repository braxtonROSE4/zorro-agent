"""
Shared platform registry for Zorro Agent.

Single source of truth for platform metadata consumed by both
skills_config (label display) and tools_config (default toolset
resolution).  Import ``PLATFORMS`` from here instead of maintaining
duplicate dicts in each module.
"""

from collections import OrderedDict
from typing import NamedTuple


class PlatformInfo(NamedTuple):
    """Metadata for a single platform entry."""
    label: str
    default_toolset: str


# Ordered so that TUI menus are deterministic.
PLATFORMS: OrderedDict[str, PlatformInfo] = OrderedDict([
    ("cli",            PlatformInfo(label="🖥️  CLI",            default_toolset="zorro-cli")),
    ("telegram",       PlatformInfo(label="📱 Telegram",        default_toolset="zorro-telegram")),
    ("discord",        PlatformInfo(label="💬 Discord",         default_toolset="zorro-discord")),
    ("slack",          PlatformInfo(label="💼 Slack",           default_toolset="zorro-slack")),
    ("whatsapp",       PlatformInfo(label="📱 WhatsApp",        default_toolset="zorro-whatsapp")),
    ("signal",         PlatformInfo(label="📡 Signal",          default_toolset="zorro-signal")),
    ("bluebubbles",    PlatformInfo(label="💙 BlueBubbles",     default_toolset="zorro-bluebubbles")),
    ("email",          PlatformInfo(label="📧 Email",           default_toolset="zorro-email")),
    ("homeassistant",  PlatformInfo(label="🏠 Home Assistant",  default_toolset="zorro-homeassistant")),
    ("mattermost",     PlatformInfo(label="💬 Mattermost",      default_toolset="zorro-mattermost")),
    ("matrix",         PlatformInfo(label="💬 Matrix",          default_toolset="zorro-matrix")),
    ("dingtalk",       PlatformInfo(label="💬 DingTalk",        default_toolset="zorro-dingtalk")),
    ("feishu",         PlatformInfo(label="🪽 Feishu",          default_toolset="zorro-feishu")),
    ("wecom",          PlatformInfo(label="💬 WeCom",           default_toolset="zorro-wecom")),
    ("wecom_callback", PlatformInfo(label="💬 WeCom Callback",  default_toolset="zorro-wecom-callback")),
    ("weixin",         PlatformInfo(label="💬 Weixin",          default_toolset="zorro-weixin")),
    ("webhook",        PlatformInfo(label="🔗 Webhook",         default_toolset="zorro-webhook")),
    ("api_server",     PlatformInfo(label="🌐 API Server",      default_toolset="zorro-api-server")),
])


def platform_label(key: str, default: str = "") -> str:
    """Return the display label for a platform key, or *default*."""
    info = PLATFORMS.get(key)
    return info.label if info is not None else default
