# 作ったツール
## md2latexpdf
MarkDown形式の文書からlatexファイルを生成し、pdfを作成するためのツール。
このスクリプトを使用するためには以下のツールが必要です。

- python3
- pandoc
- latexmk

```
# 使い方はこんな感じ
$ md2latexpdf --title '勉強会資料' --author 'toua20001' --output 'benkyoukai.pdf' benkyoukai.md
```
