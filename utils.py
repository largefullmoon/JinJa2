from typing import List

def build_headline(theme: List[str] = [], ethnicity: List[str] = [], age_range: List[int] = []) -> str:
    """
    Builds a dynamic headline for the hero section based on API keyword data.
    Accepts lists of themes, ethnicities, and age values.
    Returns a complete, human-readable string.
    """
    eth = ethnicity[0] if ethnicity else ""
    th = theme[0] if theme else ""

    age_text = ""
    if age_range and len(set(age_range)) >= 2:
        age_text = f"aged {min(age_range)}-{max(age_range)}"

    if eth and th:
        return f"Watch Hot {eth} {th}s {age_text} Live Right Now".strip()
    elif th:
        return f"Watch Live {th}s {age_text}".strip()
    elif eth:
        return f"{eth} Models Streaming Now"
    else:
        return "Thousands of Real People Are Online Right Now"

def build_subtext(theme: List[str] = [], ethnicity: List[str] = [], fetishes: List[str] = []) -> str:
    """
    Builds a subtext paragraph that supports the headline.
    Combines elements from ethnicity, theme, and optional tags (e.g. fetishes) for contextual richness.
    """
    eth_text = f"{', '.join(ethnicity)} models" if ethnicity else "real performers"
    theme_text = ", ".join(theme[:2]) if theme else ""
    fetish_text = ", ".join(fetishes[:2]) if fetishes else ""

    parts = [f"Live {eth_text}"]
    if theme_text:
        parts.append(f"into {theme_text}")
    if fetish_text:
        parts.append(f"with interests like {fetish_text}")

    return " - ".join(parts) + ". All streaming live right now."

def truncate(text: str, max_length: int = 200) -> str:
    """
    Truncates long descriptions like turn-ons or bio fields to a clean summary.
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..." 