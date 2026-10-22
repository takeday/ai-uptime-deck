# AI稼働時間を延ばす使い方 — 導入マンガ

Marp資料「AI稼働時間を延ばす使い方」の冒頭に差し込む導入マンガです。

## 1. AIにかかりきりの一日

![manga-01](manga-01.png)

## 2. 理想は、任せてあなたが違う価値を生むこと

![manga-02](manga-02.png)

## ファイル

| ファイル | 内容 |
|---|---|
| `manga/manga-01.svg`, `manga/manga-02.svg` | Marpに差し込む用のSVG（16:9） |
| `manga-01.png`, `manga-02.png` | プレビュー・PDF書き出し用のPNG |
| `intro-snippet.md` | Marpへの差し込み例 |
| `gen.py` | SVGの生成スクリプト（セリフを編集して `python3 gen.py manga` で作り直し） |

## Marpでの使い方

```markdown
![bg contain](manga/manga-01.svg)
```
