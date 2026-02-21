#!/usr/bin/env python3
"""
Team Radio - Inter-agent communication protocol
Like F1 team radio: structured, time-stamped, categorized.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class MessageType(Enum):
    HANDSHAKE = "driver_connect"
    HANDOFF = "pit_stop"
    REQUEST = "radio_message"
    RESPONSE = "copy_that"
    ALERT = "yellow_flag"
    EMERGENCY = "red_flag"
    BROADCAST = "full_course_yellow"


@dataclass
class TeamMessage:
    """A single radio transmission"""

    id: str
    timestamp: datetime
    message_type: MessageType
    from_driver: str
    to_driver: str
    priority: str
    subject: str
    content: Dict[str, Any]
    acknowledged: bool = False


class TeamRadio:
    """
    The team radio system.
    All inter-agent communication flows through here.
    """

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.messages: List[TeamMessage] = []
        self.subscribers: Dict[str, List[Callable]] = {}

    def transmit(self, message: Dict) -> str:
        """Send a message through the radio"""
        msg = TeamMessage(
            id=f"MSG-{len(self.messages) + 1:06d}",
            timestamp=datetime.now(),
            message_type=MessageType(message.get("type", "radio_message")),
            from_driver=message.get("from", "system"),
            to_driver=message.get("to", "all"),
            priority=message.get("priority", "GREEN"),
            subject=message.get("message", ""),
            content=message.get("content", {}),
        )

        self.messages.append(msg)

        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history :]

        self._notify(msg)

        return msg.id

    def subscribe(self, driver_id: str, callback: Callable):
        """Driver subscribes to messages"""
        if driver_id not in self.subscribers:
            self.subscribers[driver_id] = []
        self.subscribers[driver_id].append(callback)

    def _notify(self, message: TeamMessage):
        """Notify relevant subscribers"""
        if message.to_driver == "all":
            for callbacks in self.subscribers.values():
                for cb in callbacks:
                    cb(message)
        elif message.to_driver in self.subscribers:
            for cb in self.subscribers[message.to_driver]:
                cb(message)

    def get_recent(self, count: int = 10, driver_id: str = None) -> List[Dict]:
        """Get recent messages"""
        messages = self.messages[-count:]
        if driver_id:
            messages = [
                m
                for m in messages
                if m.from_driver == driver_id or m.to_driver == driver_id
            ]

        return [
            {
                "id": m.id,
                "timestamp": m.timestamp.isoformat(),
                "from": m.from_driver,
                "to": m.to_driver,
                "message": m.subject,
                "type": m.message_type.value,
            }
            for m in messages
        ]

    def clear(self):
        """Clear radio history"""
        self.messages = []


radio = TeamRadio()
