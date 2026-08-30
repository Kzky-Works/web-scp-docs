# 「テーマで読む」更新手順

日本語版のテーマ別記事選集は `assets/recommendations-ja.json` で管理し、`reading-ja.html` に表示する。他言語への展開は、日本語版の内容と画面が承認された後に行う。

## 掲載ルール

- 1テーマは10〜20記事とする。同じテーマ内で記事を重複させない。テーマをまたぐ重複は認める。
- 21記事目を追加したい場合は、例として「ホラー①」「ホラー②」のように分割する。単純に件数だけで割らず、各リストの内容がまとまるように分ける。
- 追加する記事IDは、すべて `assets/discovery-ja.json` に存在しなければならない。
- 公式の読書ガイド、コミュニティの選定リスト、個人の推薦記事を参考にできる。紹介文は転載せず、SCP Docs用に記述する。
- 更新時は `updatedAt` と `references` も確認する。記事の件数はページ本文へ固定値として書かない。

## 確認

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.cjs
node --check assets/reading-lists.js
```

公開前に、PCとiPhone相当の幅でテーマ切り替えを確認する。iPhone・iPadでは記事リンクが `scpdocs://open` を開き、現在のブラウザページを公式Wikiへ遷移させないことも確認する。
