"""ConAgent — the skeptic debater (loads skill_con, argues NET NEGATIVE)."""

from __future__ import annotations

from cosmos77_ex02.agents.debater import DebaterAgent


class ConAgent(DebaterAgent):
    """The Con side: social media is a net negative for society."""

    ROLE = "con"
    SKILL_FILE = "skill_con.md"
    POSITION_KEY = "debate.con_position"
