# This helper script loads localization files and exposes them to the
# bundled Bilingual Localization javascript.

import json
import os
from pathlib import Path

import gradio as gr
from modules import script_callbacks, shared

localizations = {}
ROOT_DIR = Path().absolute()
EXTENSION_DIR = Path(__file__).resolve().parents[1]
FORGE_NEO_DIR = EXTENSION_DIR / "forge_neo"
FORGE_NEO_MERGED = FORGE_NEO_DIR / ".generated_ja_JP.json"

try:
    localizations_dir = shared.cmd_opts.localizations_dir
except AttributeError:
    localizations_dir = "localizations"


def forge_neo_overlays():
    if not FORGE_NEO_DIR.is_dir():
        return []

    base_overlay = FORGE_NEO_DIR / "ja_JP.json"
    overlays = [base_overlay] if base_overlay.is_file() else []
    overlays.extend(sorted(path for path in FORGE_NEO_DIR.glob("*_ja_JP.json") if path.is_file()))
    return overlays


def build_forge_neo_merged(base_path):
    """Create one merged file for the bundled bilingual translator.

    Forge Classic neo's native localization loader can merge several ja_JP
    files itself. The bundled bilingual translator reads only one JSON file,
    so merge every Forge overlay into a generated file for that code path.
    """
    overlays = forge_neo_overlays()
    if not overlays:
        return base_path

    try:
        with open(base_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for overlay in overlays:
            with overlay.open("r", encoding="utf-8") as file:
                data.update(json.load(file))

        with FORGE_NEO_MERGED.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.write("\n")
        return str(FORGE_NEO_MERGED)
    except Exception as exc:
        print(f"[ja_JP] Failed to build Forge neo bilingual localization: {exc}")
        return base_path


def list_localizations(dirname):
    localizations.clear()

    for file in os.listdir(dirname):
        fn, ext = os.path.splitext(file)
        if ext.lower() != ".json":
            continue
        localizations[fn] = os.path.join(dirname, file)

    from modules import scripts

    for file in scripts.list_scripts("localizations", ".json"):
        fn, ext = os.path.splitext(file.filename)
        localizations[fn] = file.path

    base = localizations.get("ja_JP")
    if base:
        localizations["ja_JP"] = build_forge_neo_merged(base)


list_localizations(localizations_dir)


def relative_path(path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(ROOT_DIR.resolve()).as_posix())
    except ValueError:
        return str(path.as_posix())


def i18n_dirs():
    return {key: relative_path(value) for key, value in localizations.items()}


# Register extension options
def on_ui_settings():
    BL_SECTION = ("bl", "Bilingual Localization")

    shared.opts.add_option(
        "bilingual_localization_enabled",
        shared.OptionInfo(True, "Enable Bilingual Localization", section=BL_SECTION),
    )
    shared.opts.add_option(
        "bilingual_localization_logger",
        shared.OptionInfo(False, "Enable Devtools Log", section=BL_SECTION),
    )
    shared.opts.add_option(
        "bilingual_localization_file",
        shared.OptionInfo(
            "None",
            "Localization file (Please leave `User interface` - `Localization` as None)",
            gr.Dropdown,
            lambda: {"choices": ["None"] + list(localizations.keys())},
            refresh=lambda: list_localizations(localizations_dir),
            section=BL_SECTION,
        ),
    )
    shared.opts.add_option(
        "bilingual_localization_order",
        shared.OptionInfo(
            "Translation First",
            "Translation display order",
            gr.Radio,
            {"choices": ["Translation First", "Original First"]},
            section=BL_SECTION,
        ),
    )
    shared.opts.add_option(
        "bilingual_localization_dirs",
        shared.OptionInfo(
            json.dumps(i18n_dirs()),
            "Localization dirs",
            section=BL_SECTION,
            component_args={"visible": False},
        ),
    )


script_callbacks.on_ui_settings(on_ui_settings)
