"""Microsoft Teams platform adapter.

Connects Zorro Agent to Microsoft Teams via the Azure Bot Framework.
Receives messages through an HTTP webhook and sends replies via the
Bot Framework REST API.

Requirements:
    pip install botbuilder-core botbuilder-integration-aiohttp

Environment variables:
    TEAMS_APP_ID          — Microsoft App ID (from Azure Bot registration)
    TEAMS_APP_PASSWORD    — Client secret (from Azure Bot registration)
    TEAMS_WEBHOOK_HOST    — Bind address (default: 0.0.0.0)
    TEAMS_WEBHOOK_PORT    — Bind port (default: 3978)
    TEAMS_ALLOWED_USERS   — Comma-separated allowed user emails (optional)
    TEAMS_ALLOW_ALL_USERS — "true" to allow any user (default: false)
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional

from gateway.platforms.base import (
    BasePlatformAdapter,
    MessageEvent,
    MessageType,
    SendResult,
)

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 28_000  # Teams message size limit (chars)
DEFAULT_WEBHOOK_HOST = "0.0.0.0"
DEFAULT_WEBHOOK_PORT = 3978


def check_teams_requirements() -> bool:
    """Check if Teams dependencies are available."""
    try:
        import botbuilder.core  # noqa: F401
        import aiohttp  # noqa: F401
    except ImportError:
        return False
    app_id = os.getenv("TEAMS_APP_ID", "")
    app_password = os.getenv("TEAMS_APP_PASSWORD", "")
    return bool(app_id and app_password)


class TeamsAdapter(BasePlatformAdapter):
    """Microsoft Teams bot adapter using Azure Bot Framework."""

    MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH

    def __init__(self, config):
        from gateway.config import Platform
        super().__init__(config, Platform.TEAMS)

        extra = config.extra or {}
        self.app_id = extra.get("app_id") or os.getenv("TEAMS_APP_ID", "")
        self.app_password = extra.get("app_password") or os.getenv("TEAMS_APP_PASSWORD", "")
        self.webhook_host = extra.get("webhook_host") or os.getenv(
            "TEAMS_WEBHOOK_HOST", DEFAULT_WEBHOOK_HOST
        )
        self.webhook_port = int(
            extra.get("webhook_port") or os.getenv("TEAMS_WEBHOOK_PORT", str(DEFAULT_WEBHOOK_PORT))
        )

        # Bot Framework adapter and conversation references (populated on first message)
        self._bf_adapter = None
        self._conversation_refs: Dict[str, object] = {}
        self._runner = None
        self._site = None

    async def connect(self) -> bool:
        """Start the webhook server for Bot Framework messages."""
        try:
            from botbuilder.core import (
                BotFrameworkAdapter,
                BotFrameworkAdapterSettings,
                TurnContext,
            )
            from aiohttp import web
        except ImportError:
            logger.error("Teams: botbuilder-core or aiohttp not installed")
            return False

        settings = BotFrameworkAdapterSettings(
            app_id=self.app_id,
            app_password=self.app_password,
        )
        self._bf_adapter = BotFrameworkAdapter(settings)

        # Error handler
        async def on_error(context: TurnContext, error: Exception):
            logger.error("Teams bot error: %s", error)
            try:
                await context.send_activity("An internal error occurred.")
            except Exception:
                pass

        self._bf_adapter.on_turn_error = on_error

        # Webhook handler
        async def handle_messages(req: web.Request) -> web.Response:
            if req.content_type != "application/json":
                return web.Response(status=415)
            body = await req.text()
            try:
                from botbuilder.schema import Activity
                activity = Activity().deserialize(json.loads(body))
            except Exception as e:
                logger.warning("Teams: failed to parse activity: %s", e)
                return web.Response(status=400)

            auth_header = req.headers.get("Authorization", "")

            async def _turn_callback(turn_context: TurnContext):
                await self._handle_activity(turn_context)

            try:
                await self._bf_adapter.process_activity(
                    activity, auth_header, _turn_callback
                )
            except Exception as e:
                logger.error("Teams: process_activity failed: %s", e)
                return web.Response(status=401, text=str(e))

            return web.Response(status=200)

        app = web.Application()
        app.router.add_post("/api/messages", handle_messages)

        self._runner = web.AppRunner(app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, self.webhook_host, self.webhook_port)
        await self._site.start()

        logger.info(
            "Teams: webhook listening on %s:%s/api/messages",
            self.webhook_host,
            self.webhook_port,
        )
        return True

    async def disconnect(self):
        """Stop the webhook server."""
        if self._site:
            await self._site.stop()
            self._site = None
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
        self._bf_adapter = None
        self._conversation_refs.clear()
        logger.info("Teams: disconnected")

    async def send(self, chat_id: str, text: str, **kwargs) -> SendResult:
        """Send a text message to a Teams conversation."""
        ref = self._conversation_refs.get(chat_id)
        if not ref or not self._bf_adapter:
            return SendResult(success=False, error="No conversation reference for this chat")

        from botbuilder.core import TurnContext
        from botbuilder.schema import Activity, ActivityTypes

        sent_id = None

        async def _send_callback(turn_context: TurnContext):
            nonlocal sent_id
            # Chunk if needed
            chunks = self._chunk_text(text, self.MAX_MESSAGE_LENGTH)
            for chunk in chunks:
                response = await turn_context.send_activity(
                    Activity(type=ActivityTypes.message, text=chunk)
                )
                if response and response.id:
                    sent_id = response.id

        try:
            await self._bf_adapter.continue_conversation(
                ref, _send_callback, self.app_id
            )
            return SendResult(success=True, message_id=sent_id)
        except Exception as e:
            logger.error("Teams: send failed: %s", e)
            return SendResult(success=False, error=str(e))

    async def send_typing(self, chat_id: str):
        """Send a typing indicator."""
        ref = self._conversation_refs.get(chat_id)
        if not ref or not self._bf_adapter:
            return

        from botbuilder.core import TurnContext
        from botbuilder.schema import Activity, ActivityTypes

        async def _typing_callback(turn_context: TurnContext):
            await turn_context.send_activity(
                Activity(type=ActivityTypes.typing)
            )

        try:
            await self._bf_adapter.continue_conversation(
                ref, _typing_callback, self.app_id
            )
        except Exception:
            pass

    async def send_image(
        self, chat_id: str, image_url: str, caption: str = None
    ) -> SendResult:
        """Send an image as a hero card attachment."""
        ref = self._conversation_refs.get(chat_id)
        if not ref or not self._bf_adapter:
            return SendResult(success=False, error="No conversation reference")

        from botbuilder.core import TurnContext, CardFactory
        from botbuilder.schema import (
            Activity,
            ActivityTypes,
            HeroCard,
            CardImage,
        )

        sent_id = None

        async def _image_callback(turn_context: TurnContext):
            nonlocal sent_id
            card = HeroCard(
                title=caption or "",
                images=[CardImage(url=image_url)],
            )
            attachment = CardFactory.hero_card(card)
            response = await turn_context.send_activity(
                Activity(
                    type=ActivityTypes.message,
                    attachments=[attachment],
                    text=caption or "",
                )
            )
            if response and response.id:
                sent_id = response.id

        try:
            await self._bf_adapter.continue_conversation(
                ref, _image_callback, self.app_id
            )
            return SendResult(success=True, message_id=sent_id)
        except Exception as e:
            return SendResult(success=False, error=str(e))

    async def get_chat_info(self, chat_id: str) -> dict:
        """Return basic chat metadata."""
        ref = self._conversation_refs.get(chat_id)
        chat_type = "unknown"
        name = chat_id
        if ref:
            conv = getattr(ref, "conversation", None)
            if conv:
                name = getattr(conv, "name", None) or chat_id
                is_group = getattr(conv, "is_group", False)
                chat_type = "group" if is_group else "dm"
        return {"name": name, "type": chat_type, "chat_id": chat_id}

    # ── Internal ──────────────────────────────────────────────

    async def _handle_activity(self, turn_context):
        """Process an inbound Bot Framework activity."""
        from botbuilder.schema import ActivityTypes

        activity = turn_context.activity
        if activity.type != ActivityTypes.message:
            return
        if not activity.text:
            return

        # Store conversation reference for proactive messaging
        chat_id = activity.conversation.id if activity.conversation else ""
        if chat_id:
            from botbuilder.core import TurnContext as TC
            self._conversation_refs[chat_id] = TC.get_conversation_reference(activity)

        sender_id = ""
        sender_name = ""
        if activity.from_property:
            sender_id = activity.from_property.id or ""
            sender_name = activity.from_property.name or ""

        # Build event and dispatch
        source = self.build_source(
            chat_id=chat_id,
            user_id=sender_id,
            user_name=sender_name,
        )

        event = MessageEvent(
            source=source,
            text=activity.text,
            message_type=MessageType.TEXT,
            message_id=activity.id or "",
            raw=activity,
        )

        await self.handle_message(event)

    @staticmethod
    def _chunk_text(text: str, limit: int) -> List[str]:
        """Split text into chunks that fit within the message length limit."""
        if len(text) <= limit:
            return [text]
        chunks = []
        while text:
            if len(text) <= limit:
                chunks.append(text)
                break
            # Try to split at last newline within limit
            split_at = text.rfind("\n", 0, limit)
            if split_at <= 0:
                split_at = limit
            chunks.append(text[:split_at])
            text = text[split_at:].lstrip("\n")
        return chunks
