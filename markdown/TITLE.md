# まえがき {-}

この本は、筆者がCadSoft Eagle(**バージョン７**)のsch/brdファイルをCIで
自動レンダリングしたいと考え、ファイル構造を調べた結果のレポートです。
筆者の予想ではしかしこんなものはきっとすでにどこかの誰かがブログなりにまとめているに
違いないのですが、あえてN番煎じの内容を書きます・した。主に筆者自身のためです。

実際のファイルからXMLツリーを解析していこうとか考えてましたが早々に定義リストが
見つかってしまったので、このまとめ本が日本語訳のうちの一つになればいいなって思います。

EagleはすでにAutodeskに買収されバージョンも８に上がっていますが、もし現在Eagle
バージョン７をあえて使っている・または将来使う予定でいる方がいましたら、ちょっとだけ
役に立つかもしれません。
もしかしたらバージョン８系のファイルに適用できる部分もあるかもしれませんが、
筆者は８系を所有していないのでわかりません。

## この本の対象のEagleバージョン {-}
**Eagle Version 7.5.0** を対象にします。

## おことわり {-}
この本の内容は個人的なメモ程度であり、筆者は何ら責任を負わないものとします。
幸いにも1次資料が存在するので、疑問は大元のファイルを自力で解析することで解決してください。

# (`eagle.dtd`を)探せ！(仕様の)全てをそこにおいてきた！
参考のために拙作のEagleプロジェクトからschファイルを引用してみると2行目にいきなり
「ここを見ろ」と言われてしまいます。

[schファイル先頭5行](data/relay_isolator_1amp/relay_isolator_1A.sch){.listingtable type=xml to=5}

1行目でXMLファイルであることが示され、2行目に**DOCTYPE宣言**があります。
Microsoftの資料ページ[^ms-doc-dtd]によると、このDOCTYPE宣言により**ルート要素**と
**ドキュメント型定義**が指定されています。ということはこの型定義を見ればすなわち
Eagleファイルの解析やそれに基づいたオレオレ処理ができるということです。

[^ms-doc-dtd]: <https://msdn.microsoft.com/ja-jp/library/ms256059> \
"DOCTYPE 宣言は、ドキュメントのルート要素の指定、および外部ファイル、直接宣言、またはその両者を用いたドキュメント型定義 (DTD) を指定する場所を提供します。"

## eagle.dtdはどこにいるのか {-}
DTDとして指定されている`eagle.dtd`のありかを探します。`eagle.dtd`でググるとElement14の
掲示板ページが見つかります：

- https://www.element14.com/community/thread/15731/l/eagle-version-60-released

Eagleバージョン６のリリースノートを引用しているようです。すぐにDTDへの言及が見つかります。

> - The complete definition of the new EAGLE file format can be found in the file "doc/eagle.dtd".

より、`doc/eagle.dtd`を探します。Mac版では`/Applications/Eagle-7.5.0/doc/eagle.dtd`にありました。
`<Eagleのインストールディレクトリ>/doc/eagle.dtd`を探してください。

# eagle.dtdを研究しよう
## ライセンス条項 {-}
eagle.dtdは"CC BY-ND 3.0"ライセンスのもとで再配布が認められていますが、改変は禁止です。

[doc/eagle.dtdライセンス部](data/eagle.dtd){.listingtable type=xml from=2 to=13}

## 型定義
# Appendix {-}
[doc/eagle.dtd全文](data/eagle.dtd){.listingtable type=xml}
