# Stable Diffusion WebUI 日本語化 (Forge Classic neo 対応)

Stable Diffusion WebUI 向けの日本語ローカライズです。

このフォークでは、従来の AUTOMATIC1111 用 `localizations/ja_JP.json` を残したまま、[sd-webui-forge-classic](https://github.com/Haoming02/sd-webui-forge-classic) の `neo` ブランチ向け翻訳を追加しています。

## Forge Classic neo 対応状況

2026-09-09 時点で、`neo` ブランチの以下のコミットを基準に確認しています。

- `Haoming02/sd-webui-forge-classic`
- branch: `neo`
- commit: `efc42fe03739d0d8cda7de6e7bed2f8c1969a0c7`

Forge 固有部分は `forge_neo/ja_JP.json` に分離しています。Forge Classic neo は同一ロケールの複数 JSON を順番にマージできるため、起動時に `scripts/forge_classic_neo_helper.py` が既存の `ja_JP.json` の後へ Forge 用オーバーレイを追加します。

現在のオーバーレイには主に以下を含みます。

- Forge のモデル選択 UI (`UI Preset`, `VAE / Text Encoder`, `Diffusion in Low Bits` など)
- 各プリセットの設定項目
- Forge Canvas の設定・ツールバー・動的なブラシ表示
- 統合 ControlNet の UI とモード選択
- Torch Compile Integrated
- LoRA Control Integrated

従来の AUTOMATIC1111 側の翻訳ファイルを丸ごと置き換えない構成なので、既存訳を維持しつつ Forge 固有文字列だけを更新できます。

Forge Canvas の `Brush Width (25)` のように値を含んで変化する表示には `@@` で始まる正規表現キーを使用します。Forge Classic neo の標準Localizationは完全一致のみのため、`javascript/forge_neo_regex_localization.js` がネイティブLocalizationでもこれらのキーを処理します。

## インストール

WebUI の `Extensions` → `Install from URL` から、このリポジトリをインストールします。

```text
https://github.com/turbo-boo/stable-diffusion-webui-localization-ja_JP
```

インストール後、WebUI を再起動してください。

## 通常の日本語化

1. `Settings` → `User interface` を開く
2. `Localization` で `ja_JP` を選択する
3. 設定を適用し、UI を再読み込みする

Forge Classic neo では、ベースの `localizations/ja_JP.json` と `forge_neo/ja_JP.json` が同じ `ja_JP` として読み込まれます。

## Bilingual Localization

このリポジトリに含まれる Bilingual Localization も Forge Classic neo 用オーバーレイに対応しています。

Bilingual Localization は単一の JSON を読み込む実装のため、`scripts/bilingual_localization_helper.py` が起動時にベース翻訳と Forge 用オーバーレイを結合し、`forge_neo/.generated_ja_JP.json` を生成します。この生成ファイルは Git 管理対象外です。

Bilingual Localization を使う場合は、通常の `Settings` → `User interface` → `Localization` を `None` にし、`Settings` → `Bilingual Localization` から `ja_JP` を選択してください。

## ファイル構成

```text
localizations/
└─ ja_JP.json                         # 従来の日本語訳

forge_neo/
└─ ja_JP.json                         # Forge Classic neo 固有の追加・上書き翻訳

scripts/
├─ forge_classic_neo_helper.py        # Forge native localization へオーバーレイを追加
└─ bilingual_localization_helper.py   # Bilingual 用にベース + Forge を結合

javascript/
└─ forge_neo_regex_localization.js    # native localization で @@regex を処理
```

## 翻訳の追加・修正

共通 UI の翻訳は `localizations/ja_JP.json`、Forge Classic neo 固有 UI の翻訳は `forge_neo/ja_JP.json` を編集してください。

Forge の通常の UI 文字列は完全一致で参照されるため、大文字・小文字や句読点が変わった場合は別キーとして追加する必要があります。値を含んで動的に変化する表示には `@@` 正規表現キーを使用できます。

## Credits

このプロジェクトは従来の Stable Diffusion WebUI 日本語化プロジェクトと、その翻訳資産を基にしています。

- [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Haoming02/sd-webui-forge-classic](https://github.com/Haoming02/sd-webui-forge-classic)
- [journey-ad/sd-webui-bilingual-localization](https://github.com/journey-ad/sd-webui-bilingual-localization)
- [harukaxxxx/stable-diffusion-webui-localization-source](https://github.com/harukaxxxx/stable-diffusion-webui-localization-source)

ライセンスについては `LICENSE` を参照してください。
