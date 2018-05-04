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
|               |            |
<!--  -->
| attribute |  type  | required |
|-----------|--------|----------|
| version   | _Real_ | Yes      |

[](data/eagle.dtd){.listingtable type=xml from=52 to=56}

### //eagle/compatibility {-}

文字列要素です。`eagle`タグに書かれたものと異なるバージョンのEagleでファイルを開いたり編集した場合に更新されると思われます。
<!-- attr=属性 -->
| Sub element | Appearance |
|-------------|------------|
| note        | 0~         |

#### //eagle/compatibility/note {-}

| attribute |    type    | required |
|-----------|------------|----------|
| version   | _Real_     | Yes      |
| severity  | _Severity_ | Yes      |

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
当該部品だけ切り出しされてきます。切り出されるものは回路図シンボルとレイアウト両方です。

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

ライブラリを使わず直接描かれたオブジェクトがまとめられます。Netレイヤで描かれた図形は`nets`要素以下に置かれます。

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

## ライブラリ要素と直下の子要素たち
### .../library/packages {-}
### .../library/symbols {-}
### .../library/symbols/symbol {-}

回路図シンボル要素です。

[](data/eagle.dtd){.listingtable type=xml from=103 to=106}

| Sub element | Appearance |
|-------------|------------|
| description | 0~1        |
| polygon     | 0~         |
| wire        | 0~         |
| text        | 0~         |
| dimension   | 0~         |
| pin         | 0~         |
| circle      | 0~         |
| rectangle   | 0~         |
| frame       | 0~         |
<!--  -->
| attribute |   type   | required | default |
|-----------|----------|----------|---------|
| name      | _String_ | Yes      |         |

#### .../library/symbols/symbol/pin {-}

回路図エディタ上で配線をつなげる"ピン"の要素です。属性のうち`direction`/`swaplevel`の内容は
図形の描画だけを目標とするときには気にしなくていいと思われます。

実際の描画は始点$(x,y)$から右方向に水平線分を描きます。線分の長さは`length`が _pin_/_short_/_middle_/_long_ の順で
0/1/2/3 * 2.54mm(0.1インチ)です。
`visible`スイッチの内容が*pin*または*both*のとき、線分の終点から2.50mmくらいのところから`name`の内容を書きます。
*pad*または*both*のとき、線分の上または左にピン番号を書きます。ピン番号は`deviceset`要素以下の`connect`子要素の内容を
参照する必要があります。

[](data/eagle.dtd){.listingtable type=xml from=353 to=364}

| attribute |      type      | required | default |
|-----------|----------------|----------|---------|
| name      | _String_       | Yes      |         |
| x         | _Coord_        | Yes      |         |
| y         | _Coord_        | Yes      |         |
| visible   | _PinVisible_   |          | "both"  |
| length    | _PinLength_    |          | "long"  |
| direction | _PinDirection_ |          | "io"    |
| function  | _PinFunction_  |          | "none"  |
| swaplevel | _Int_          |          | "0"     |
| rotation  | _Rotation_     |          | "R0"    |

### .../library/devicesets {-}
### .../library/devicesets/deviceset {-}
## 各種図形要素たち
### .../sheet/*/polygon {-}

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

### .../sheet/*/polygon/vertex {-}

[](data/eagle.dtd){.listingtable type=xml from=345 to=351}

| attribute |    type     | required | default |                      note                      |
|-----------|-------------|----------|---------|------------------------------------------------|
| x         | _Coord_     | Yes      |         |                                                |
| y         | _Coord_     | Yes      |         |                                                |
| curve     | _WireCurve_ |          | "0"     | The curvature from this vertex to the next one |

### .../sheet/*/wire {-}

$(x1,y1)$と$(x2,y2)$を結ぶ線分要素です。線分は直線だけではなく弧を含みます。$curve>0$のとき始点から反時計回りの弧を描きます。
$(x1,y1)=(0,0), (x2,y2)=(10,0),curve=180$なら*下に凸の半円*です。

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

### .../sheet/*/text {-}

テキスト要素です。座標$(x,y)$はアンカー位置です。align属性の値によって変わります。
テキストの内容に`!`が含まれる場合は`!`と{`!`または改行(`\\n`)}に挟まれた範囲それぞれに上線がつきます。正規表現だと`/!([^!\\n]*)[!\\n]/g`です。

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

### .../sheet/*/circle {-}

[](data/eagle.dtd){.listingtable type=xml from=232 to=239}

| attribute |    type     | required | default |
|-----------|-------------|----------|---------|
| x         | _Coord_     | Yes      |         |
| y         | _Coord_     | Yes      |         |
| radius    | _Coord_     | Yes      |         |
| width     | _Dimension_ | Yes      |         |
| layer     | _Layer_     | Yes      |         |

### .../sheet/*/rectangle {-}

$(x1,y1)$から$(x2,y2)$までの塗りつぶし矩形要素です。

[](data/eagle.dtd){.listingtable type=xml from=241 to=249}

| attribute |    type    | required | default |
|-----------|------------|----------|---------|
| x1        | _Coord_    | Yes      |         |
| y1        | _Coord_    | Yes      |         |
| x2        | _Coord_    | Yes      |         |
| y2        | _Coord_    | Yes      |         |
| layer     | _Layer_    | Yes      |         |
| rot       | _Rotation_ |          | "R0"    |

### .../sheet/*/frame {-}

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
