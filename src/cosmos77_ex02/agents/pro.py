"""ProAgent — the optimist debater (loads skill_pro, argues NET POSITIVE)."""

from __future__ import annotations

from cosmos77_ex02.agents.debater import DebaterAgent


class ProAgent(DebaterAgent):
    """The Pro side: social media is a net positive for society."""

    ROLE = "pro"
    SKILL_FILE = "skill_pro.md"
    POSITION_KEY = "debate.pro_position"
