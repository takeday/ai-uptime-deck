# AI稼働時間を延ばす使い方 — 導入マンガ

Marp資料「AI稼働時間を延ばす使い方」の冒頭に差し込む導入マンガです。

## 1. AIにかかりきりの一日

![manga-01](manga-01.png)

## 2. 理想は、任せてあなたが違う価値を生むこと

![manga-02](manga-02.png)

## 3. 主旨4項目

### ① Workflowでチェック系をまとめて任せる
![manga-03](manga-03.png)

### ② /loop で巡回させて、日課を自動化する
![manga-04](manga-04.png)

### ③ すぐ答えられる問いから返して、裏で進めさせる
![manga-05](manga-05.png)

### ④ 段取りを固めて、オープンクエスチョンをさせない
![manga-06](manga-06.png)

## 中国語版（简体中文）

[`zh/`](zh/) に同じ6ページの簡体字版があります（`zh/manga-01.png` 〜 `zh/manga-06.png`、Marp用SVGは `zh/manga/`）。

![zh-manga-01](zh/manga-01.png)

## ファイル

| ファイル | 内容 |
|---|---|
| `manga/manga-01.svg` 〜 `manga/manga-06.svg` | Marpに差し込む用のSVG（16:9）。01-02が導入、03-06が主旨4項目 |
| `manga-01.png` 〜 `manga-06.png` | プレビュー・PDF書き出し用のPNG |
| `zh/` | 中国語（簡体字）版。`python3 build_zh.py` で日本語版から再生成 |
| `intro-snippet.md` | Marpへの差し込み例 |
| `gen.py`, `gen_points.py` | SVGの生成スクリプト（セリフを編集して `python3 gen.py manga` / `python3 gen_points.py manga` で作り直し） |

## Marpでの使い方

```markdown
![bg contain](manga/manga-01.svg)
```
