"""Load Forge Classic neo-specific translations as overlays for ja_JP.

Forge Classic neo keeps a list of JSON files for each localization and merges
those files in order. Older A1111 builds used a single string path instead, so
this script intentionally does nothing there.
"""

from pathlib import Path


def forge_neo_overlays():
    root = Path(__file__).resolve().parents[1] / "forge_neo"
    if not root.is_dir():
        return []

    base_overlay = root / "ja_JP.json"
    overlays = [base_overlay] if base_overlay.is_file() else []
    overlays.extend(
        sorted(
            path
            for path in root.glob("*_ja_JP.json")
            if path.is_file() and not path.name.startswith(".")
        )
    )
    return overlays


def register_forge_neo_overlays():
    try:
        from modules import localization
    except Exception:
        return

    files = localization.localizations.get("ja_JP")
    if not isinstance(files, list):
        return

    for overlay in forge_neo_overlays():
        overlay_path = str(overlay)
        if overlay_path not in files:
            files.append(overlay_path)


register_forge_neo_overlays()
