# まえがき {-}

この本は、筆者がCadSoft Eagle(**バージョン７**)のsch/brdファイルをCIで
自動レンダリングしたいと考え、ファイル構造を調べた結果のレポートです。
筆者の予想ではしかしこんなものはきっとすでにどこかの誰かがブログなりにまとめているに
違いないのですが[^python-lib-exists]、あえてN番煎じの内容を書きます・した。主に筆者自身のためです。

[^python-lib-exists]: https://github.com/at-wat/eagle2svg など

実際のファイルからXMLツリーを解析していこうとか考えてましたが早々に定義リストが
見つかってしまったので、このまとめ本がDTDの日本語訳の一つになればいいなって思います。

EagleはすでにAutodeskに買収されバージョンも８に上がっていますが、もし現在Eagle
バージョン７をあえて使っている・または将来使う予定でいる方がいましたら、ちょっとだけ
役に立つかもしれません。
もしかしたらバージョン８系のファイルに適用できる部分もあるかもしれませんが、
筆者は８系を所有していないのでわかりません。

## この本の対象のEagleバージョン {-}
**Eagle Version 7.5.0** を対象にします。

## この本のゴール {-}
この本では、回路図ファイル(schファイル)からSVG画像を出力することをゴールとします。
レイアウトファイル(brdファイル)は基本的に対象外にします。

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
Eagleファイルの解析やそれに基づいたオレオレ処理[^extra-process]ができるということです。

[^ms-doc-dtd]: <https://msdn.microsoft.com/ja-jp/library/ms256059> \\
"DOCTYPE 宣言は、ドキュメントのルート要素の指定、および外部ファイル、直接宣言、
またはその両者を用いたドキュメント型定義(DTD) を指定する場所を提供します。"
[^extra-process]: brdファイルを読み込んで自動的に面付けして別ファイルに出力するプログラムとか、
ライブラリを更新してリポジトリにプッシュするとAttributeが自動更新されるCI設定とか、
AtomとかVSCodeのビューアプラグイン書けるとかゆめがひろがりんぐ（？）

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

[doc/eagle.dtdライセンス部](data/eagle.dtd){.listingtable type=plain from=1 to=14}

## 型定義
型定義部はとりあえず後回しにします。

[doc/eagle.dtd型定義部](data/eagle.dtd){.listingtable type=xml from=16 to=48}

## ルート要素と直下の子要素たち
### //eagle {-}
ルート要素です。`compatibility`要素（0または1回出現）、`drawing`要素（必ず、1回出現）、
`compatibility`要素（0または1回出現）をこの順序で子要素に持ちます。

|  Sub element  | Appearance |
|---------------|------------|
| compatibility | 0~1        |
| drawing       | 1          |
| compatibility | 0~1        |
<!--  -->
|   attribute   |    type    | required |
|---------------|------------|----------|
| version       | _Real_     | Yes      |

[](data/eagle.dtd){.listingtable type=xml from=52 to=56}

### //eagle/compatibility {-}
文字列要素です。`eagle`タグに書かれたものと異なるバージョンのEagleでファイルを開いたり編集した場合に更新されると思われます。
<!-- attr=属性 -->
| Sub element | Appearance |
|-------------|------------|
| note        | 0~         |

#### //eagle/compatibility/note {-}

|   attribute   |    type    | required |
|---------------|------------|----------|
| version       | _Real_     | Yes      |
| severity      | _Severity_ | Yes      |

[](data/eagle.dtd){.listingtable type=xml from=58 to=65}

### //eagle/drawing {-}
描画情報の要素です。設定情報(`settings`,`gtid`,`layers`)と`library/schematic/board`の
いずれかを子要素に持ちます。

|          Sub element          | Appearance |
|-------------------------------|------------|
| settings                      | 0~1        |
| grid                          | 0~1        |
| layers                        | 1          |
| library or schematic or board | 1          |

[](data/eagle.dtd){.listingtable type=xml from=67 to=67}

### //eagle/drawing/schematic {-}
回路図情報を持つ要素です。

[](data/eagle.dtd){.listingtable type=xml from=75 to=79}

| Sub element | Appearance |
|-------------|------------|
| description | 0~1        |
| libraries   | 0~1        |
| attributes  | 0~1        |
| variantdefs | 0~1        |
| classes     | 0~1        |
| modules     | 0~1        |
| parts       | 0~1        |
| sheets      | 0~1        |
| errors      | 0~1        |
<!--  -->
| attribute |   type   | required |
|-----------|----------|----------|
| xreflabel | _String_ | Optional |
| xrefpart  | _String_ | Optional |

ブランクファイルを試しに作ったところ、`errors`と`description`以外の子要素が
用意されました。それぞれの子要素はブランクまたはデフォルト値が格納されています。

[untitle.sch（抜粋）](data/untitled.sch){.listingtable type=xml from=21 to=46}

## 回路図要素直下の子要素たち
### .../schematic/libraries {-}
librariesはlibraryの配列要素です。

[](data/eagle.dtd){.listingtable type=xml from=480 to=480}

| Sub element | Appearance |
|-------------|------------|
| library     | 0~         |

### .../schematic/libraries/library {-}
回路図に部品を置くと追加されます。追加される内容はそのライブラリまるごとではなく、
当該部品だけ切り出しされてきます。

[](data/eagle.dtd){.listingtable type=xml from=69 to=73}

| Sub element | Appearance |
|-------------|------------|
| description | 0~1        |
| packages    | 0~1        |
| symbols     | 0~1        |
| devicesets  | 0~1        |

### .../schematic/parts {-}

| Sub element | Appearance |
|-------------|------------|
| part        | 0~         |

[](data/eagle.dtd){.listingtable type=xml from=485 to=485}

### .../schematic/parts/part {-}

| Sub element | Appearance |
|-------------|------------|
| attribute   | 0~         |
| variant     | 0~         |
<!--  -->
| attribute  |   type   | required | default |
|------------|----------|----------|---------|
| name       | _String_ | Yes      |         |
| library    | _String_ | Yes      |         |
| deviceset  | _String_ | Yes      |         |
| device     | _String_ | Yes      |         |
| technology | _String_ | Optional | ""      |
| value      | _String_ | Optional |         |

### .../schematic/sheets {-}
sheetsはsheetの配列要素です[^non-commercial-license]。

[](data/eagle.dtd){.listingtable type=xml from=473 to=473}

| Sub element | Appearance |
|-------------|------------|
| sheet       | 0~         |

[^non-commercial-license]: 非営利ライセンスでは１シートしか使えないのでsheetは１度だけ登場します。

#### .../schematic/sheets/sheet {-}

[](data/eagle.dtd){.listingtable type=xml from=96 to=96}

| Sub element | Appearance |
|-------------|------------|
| description | 0~1        |
| plain       | 0~1        |
| moduleinsts | 0~1        |
| instances   | 0~1        |
| busses      | 0~1        |
| nets        | 0~1        |

## シート要素と直下の子要素たち
### .../sheet/plain {-}
ライブラリを使わず直接描かれたオブジェクトがまとめられます。

[](data/eagle.dtd){.listingtable type=xml from=488 to=488}

| Sub element | Appearance |
|-------------|------------|
| polygon     | 0~         |
| wire        | 0~         |
| text        | 0~         |
| dimension   | 0~         |
| circle      | 0~         |
| rectangle   | 0~         |
| frame       | 0~         |
| hole        | 0~         |

### .../sheet/instances {-}
instancesはinstanceの配列要素です。

[](data/eagle.dtd){.listingtable type=xml from=486 to=486}

| Sub element | Appearance |
|-------------|------------|
| polygon     | 0~         |

#### .../sheet/instances/instance {-}
実際に置かれた部品の情報がまとめられます。`part`属性は"C1"とか"R10"とか"IC2"などの呼び名が
格納されています。`gate`は複数の部品をひとかたまりにしたライブラリを使っているときの、
各々の部品名("G$1"など)です。`x`と`y`属性は回路図上の座標です。この座標を部品の中心として、
`.../schematic/libraries/library`から描画していけば線分だけの部品シンボルであれば描画できそうです。

[](data/eagle.dtd){.listingtable type=xml from=384 to=393}

| Sub element | Appearance |
|-------------|------------|
| attribute   | 0~         |
<!--  -->
| attribute |    type    | required | default |
|-----------|------------|----------|---------|
| part      | _String_   | Yes      |         |
| gate      | _String_   | Yes      |         |
| x         | _Coord_    | Yes      |         |
| y         | _Coord_    | Yes      |         |
| smashed   | _Bool_     | Optional | "no"    |
| rot       | _Rotation_ | Optional | "R0"    |

### .../sheet/buses {-}
### .../sheet/nets {-}
ひとことでいうといわゆる**ネットリスト**がここに置かれます。

[](data/eagle.dtd){.listingtable type=xml from=493 to=493}

| Sub element | Appearance |
|-------------|------------|
| net         | 0~         |

#### .../sheet/nets/net {-}

[](data/eagle.dtd){.listingtable type=xml from=126 to=130}

| Sub element | Appearance |
|-------------|------------|
| segment     | 0~         |

## 各種図形要素たち
### .../sheet/plain/polygon {-}

[](data/eagle.dtd){.listingtable type=xml from=328 to=343}

| Sub element | Appearance |
|-------------|------------|
| vertex      | 0~         |
<!--  -->
| attribute |     type      | required | default |                           note                            |
|-----------|---------------|----------|---------|-----------------------------------------------------------|
| width     | _Dimension_   | Yes      |         |                                                           |
| layer     | _Layer_       | Yes      |         |                                                           |
| spacing   | _Dimension_   | Optional |         |                                                           |
| pour      | _PolygonPour_ | Yes      | "solid" |                                                           |
| isolate   | _Dimension_   | Optional |         | Only in `<signal>` or `<package>` context                 |
| orphans   | _Bool_        | Optional | "no"    | Only in `<signal>` context                                |
| thermals  | _Bool_        | Optional | "yes"   | Only in `<signal>` context                                |
| rank      | _Int_         | Optional | "0"     | 1..6 in `<signal>` context, 0 or 7 in `<package>` context |

### .../sheet/plain/polygon/vertex {-}

[](data/eagle.dtd){.listingtable type=xml from=345 to=351}

### .../sheet/plain/wire {-}

[](data/eagle.dtd){.listingtable type=xml from=182 to=196}

| attribute |    type     | required |   default    |                  note                  |
|-----------|-------------|----------|--------------|----------------------------------------|
| x1        | _Coord_     | Yes      |              |                                        |
| y1        | _Coord_     | Yes      |              |                                        |
| x2        | _Coord_     | Yes      |              |                                        |
| y2        | _Coord_     | Yes      |              |                                        |
| width     | _Dimension_ | Yes      |              |                                        |
| layer     | _Layer_     | Yes      |              |                                        |
| extent    | _Extent_    | Optional |              | Only applicable for airwires           |
| style     | _WireStyle_ |          | "continuous" |                                        |
| curve     | _WireCurve_ |          | "0"          |                                        |
| cap       | _WireCap_   |          | "round"      | Only applicable if 'curve' is not zero |

### .../sheet/plain/text {-}

[](data/eagle.dtd){.listingtable type=xml from=219 to=230}

| attribute |    type     | required |    default     |
|-----------|-------------|----------|----------------|
| x         | _Coord_     | Yes      |                |
| y         | _Coord_     | Yes      |                |
| size      | _Dimension_ | Yes      |                |
| layer     | _Layer_     | Yes      |                |
| font      | _TextFont_  |          | "proportional" |
| ratio     | _Int_       |          | "8"            |
| rot       | _Rotation_  |          | "R0"           |
| align     | _Align_     |          | "bottom-left"  |
| distance  | _Int_       |          | "50"           |

### .../sheet/plain/circle {-}

[](data/eagle.dtd){.listingtable type=xml from=232 to=239}

| attribute |    type     | required | default |
|-----------|-------------|----------|---------|
| x         | _Coord_     | Yes      |         |
| y         | _Coord_     | Yes      |         |
| radius    | _Coord_     | Yes      |         |
| width     | _Dimension_ | Yes      |         |
| layer     | _Layer_     | Yes      |         |

### .../sheet/plain/rectangle {-}

[](data/eagle.dtd){.listingtable type=xml from=241 to=249}

| attribute |    type    | required | default |
|-----------|------------|----------|---------|
| x1        | _Coord_    | Yes      |         |
| y1        | _Coord_    | Yes      |         |
| x2        | _Coord_    | Yes      |         |
| y2        | _Coord_    | Yes      |         |
| layer     | _Layer_    | Yes      |         |
| rot       | _Rotation_ |          | "R0"    |

### .../sheet/plain/frame {-}

[](data/eagle.dtd){.listingtable type=xml from=251 to=264}

|   attribute   |  type   | required | default |
|---------------|---------|----------|---------|
| x1            | _Coord_ | Yes      |         |
| y1            | _Coord_ | Yes      |         |
| x2            | _Coord_ | Yes      |         |
| y2            | _Coord_ | Yes      |         |
| columns       | _Int_   | Yes      |         |
| rows          | _Int_   |          |         |
| layer         | _Layer_ |          |         |
| border-left   | _Bool_  |          |         |
| border-top    | _Bool_  |          |         |
| border-right  | _Bool_  |          |         |
| border-bottom | _Bool_  |          |         |

# ライブラリと回路情報からレンダリングされる内容を作り出すには
## やってTRY（１）：シンボルの描画
### シンボルまでたどり着く
ここまで調べてみてある程度方針が固まってきました。`.../sheet/instances/instance/`以下から
`part`、`gate`、`x`、`y`を得ます。この中の`part`を使って
`.../schematic/parts/part`の該当部品を引いて`library`、`deviceset`、`device`を得ます。
得られた`library`と`deviceset`を使って`.../schematic/libraries/library/devicesets/`の中から
`deviceset`を得ます。`deviceset/gates/gate`内の`symbol`属性を使って`/schematic/libraries/library/symbols/symbol`
を得ます。これである部品のシンボルが得られるので、シンボル内の部品[^components]それぞれについて座標(`x`,`y`)を中心に描画すれば
どうやらライブラリ内のシンボルを描画することはできそうに思えます。

[^components]: _wire_/_circle_/_text_/_pin_ などです。回路図ファイルは優先順位計算がないっぽいのでポリゴンも描けると思います。

[instance to symbol query tree](data/instance-to-symbol.diag){.blockdiag}

試しにシンプルな回路を描いてみて、実際にシンボル情報までたどり着いてみます。Eagle付属のライブラリを使って
トランジスタ2石の無安定（非安定）バイブレータ[^wikipedia]を描いてみます。

![無安定（非安定）バイブレータ](images/multivibrator.png)

[^wikipedia]: <https://ja.wikipedia.org/wiki/マルチバイブレータ#非安定マルチバイブレータ回路>
<!--
```{.plantuml im_out="img" caption="PlantUML x ditaa x imagine"}
<#include "instance-to-symbol.puml">
```
 -->

<!-- # Appendix {-}
[doc/eagle.dtd全文](data/eagle.dtd){.listingtable type=xml} -->
