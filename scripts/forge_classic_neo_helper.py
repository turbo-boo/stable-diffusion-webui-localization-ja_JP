"""Load Forge Classic neo-specific translations as an overlay for ja_JP.

Forge Classic neo keeps a list of JSON files for each localization and merges
those files in order. Older A1111 builds used a single string path instead, so
this script intentionally does nothing there.
"""

from pathlib import Path


def register_forge_neo_overlay():
    try:
        from modules import localization
    except Exception:
        return

    files = localization.localizations.get("ja_JP")
    if not isinstance(files, list):
        return

    overlay = Path(__file__).resolve().parents[1] / "forge_neo" / "ja_JP.json"
    if not overlay.is_file():
        return

    overlay_path = str(overlay)
    if overlay_path not in files:
        files.append(overlay_path)


register_forge_neo_overlay()
