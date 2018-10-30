===============
Direct I/O JSON
===============

この文書では、Direct I/OでJSON形式 [#]_ および JSON Lines形式 [#]_ のテキストファイルを取り扱うための機能「Direct I/O JSON」について説明します。

..  experimental::
    Asakusa Framework バージョン |version| では、 Direct I/O JSON は試験的機能として提供しています。

..  [#] http://json.org/
..  [#] http://jsonlines.org/

概要
====

Direct I/O JSONでは、Direct I/OでJSON形式を持つテキストファイルを読み書きするための汎用的な機能を提供します。

また、JSON Lines呼ばれる、JSONの1レコードを1行で格納し、レコード間を改行で区切る形式 [2]_ もサポートしています。
JSON Lines形式の入力ファイルは分割して処理を行うことができるため、通常のJSON形式に比べて高速にファイルの入力処理を実行できる可能性があります。

Direct I/O JSONで出力するファイルの形式は、JSON Lines形式となります。

データフォーマットの作成
========================

Direct I/O JSONを利用するには、DMDLに対してDirect I/O JSONを利用することを示す拡張属性 ``@directio.json`` を追加します。

JSON形式のファイルに対応するデータモデルを定義するDMDLスクリプトの例は、以下のようになります。

..  code-block:: dmdl

    @directio.json
    document = {
        "the name of this document"
        name : TEXT;

        "the content of this document"
        content : TEXT;
    };

また、JSON Lines形式のファイルとして読み込む場合、``@directio.json`` に対して属性 ``format = jsonl`` を指定します。

..  code-block:: dmdl

    @directio.json (
        format = jsonl
    )
    document = {
        "the name of this document"
        name : TEXT;

        "the content of this document"
        content : TEXT;
    };

上記のように記述してデータモデルクラスを生成すると、 ``<出力先パッケージ>.json.<データモデル名>JsonFormat`` というクラスが自動生成されます。
このクラスは ``DataFormat`` を実装し、JSON形式のテキストファイルを取り扱えます。

また、 単純な :ref:`directio-dsl-input-description` と :ref:`directio-dsl-output-description` の骨格も自動生成します。
前者は ``<出力先パッケージ>.json.Abstract<データモデル名>JsonInputDescription`` 、後者は ``<出力先パッケージ>.json.Abstract<データモデル名>JsonOutputDescription`` というクラス名で生成します。必要に応じて継承して利用してください。

データフォーマットの設定
========================

``@directio.json`` 属性の要素には、データフォーマットに関する次のような設定を指定することができます。

* `テキスト全体の構成`_
* `データ型の形式`_
* `入力時の動作`_

ここで指定する設定項目のうち、JSONフィールドに対して適用される設定については、全てのJSONフィールドに共通の設定値として適用されます。
JSONフィールド単位で個別に設定を指定したい場合は、 後述の `JSONフィールドの設定`_ を行うことでJSONフィールド単位に設定を上書きすることができます。

以下はDMDLスクリプトの記述例です。

..  code-block:: dmdl

    @directio.json (
        format = jsonl,
        compression = "gzip",
        date_format = "yyyy/MM/dd",
        datetime_format = "yyyy/MM/dd HH:mm:ss",
        on_unknown_input = report
    )
    model = {
        ...
    };

テキスト全体の構成
------------------

``format``
  入力ファイルのJSON形式。以下のオプションから指定する。

  * ``json``  : JSON形式
  * ``jsonl`` : JSON Lines形式

  ``jsonl`` を指定して、入力ファイルがJSON Linesの形式を満たしていない場合は正常にファイルの読み込みが行われないことがある。

  出力ファイルの形式は常にJSON Lines形式となる。

  既定値: ``json``

``charset``
  ファイルの文字セットエンコーディングを表す文字列。

  指定した文字セットエンコーディングが ASCII または ASCIIの上位互換 のいずれでもない場合、 :ref:`directio-input-split` が行われなくなる。

  既定値: ``"UTF-8"``

``compression``
  ファイルの圧縮形式。 ``"gzip"`` または ``CompressionCodec`` [#]_ のサブタイプのクラス名を指定する。

  ここで指定した圧縮形式で対象のファイルが読み書きされるようになるが、代わりに :ref:`directio-input-split` が行われなくなる。

  既定値: 未指定 (圧縮無し)

``line_separator``
  ファイル出力時に使用する、レコード間を区切るテキストの改行文字。以下のオプションから指定する。

  * ``unix``    : LF のみ
  * ``windows`` : CRLF の組み合わせ

  入力時にはこの設定を利用せず、 LF, CR, CRLF のいずれも空白文字として扱う。

  既定値: ``unix``

..  [#] ``org.apache.hadoop.io.compress.CompressionCodec``

データ型の形式
--------------

``date_format``
  データモデルの日付型 ( ``DATE`` ) の形式。 ``SimpleDateFormat`` [#]_ の形式で指定する。

  既定値: ``"yyyy-MM-dd"``

``datetime_format``
  データモデルの日時型 ( ``DATETIME`` ) の形式。 ``SimpleDateFormat`` の形式で指定する。

  既定値: ``"yyyy-MM-dd HH:mm:ss"``

``null_style``
  出力時に、 対象プロパティが ``NULL`` 値であった場合の、プロパティに対応するJSONフィールドの出力内容。以下のオプションから指定する。

  * ``value``  : フィールドの値に ``null`` をセットして出力する。
  * ``absent`` : フィールドを出力しない。

  既定値: ``value``

..  [#] ``java.text.SimpleDateFormat``

入力時の動作
------------

``on_malformed_input``
  入力時に、不正な値が検出された場合の動作。以下のオプションから指定する。

  * ``error``    : エラーログを出力して、異常終了する。
  * ``report``   : 警告ログを出力して、プロパティに ``NULL`` を設定する。
  * ``ignore``   : プロパティに ``NULL`` を設定する。

  既定値: ``error``

``on_unknown_input``
  入力時に、データモデルのプロパティに対応しないキー文字列が検出された場合の動作。以下のオプションから指定する。

  * ``error``    : エラーログを出力して、異常終了する。
  * ``report``   : 警告ログを出力する。
  * ``ignore``   : 無視する。

  既定値: ``error``

``on_missing_input``
  入力時に、データモデルのプロパティに対応するキー文字列が出現しなかった場合の動作。以下のオプションから指定する。

  * ``error``    : エラーログを出力して、異常終了する。
  * ``report``   : 警告ログを出力して、プロパティに ``NULL`` を設定する。
  * ``ignore``   : プロパティに ``NULL`` を設定する。

  既定値: ``ignore``

..  attention::
    ``null_style`` に ``absent`` を指定し、かつ ``on_missing_input`` に ``error`` を指定した場合、 ``NULL`` 値を持つプロパティに対して対称性が失われるので注意が必要です。

    上記の設定を持つデータモデルをJSONファイルとして出力する場合、NULL値を持つプロパティは ``null_style = absent`` によってJSONフィールドには含まれません。
    その後、出力したJSONファイルを同じデータモデルとして入力すると、プロパティに対応するJSONフィールドが存在しないこととなり、 ``on_missing_input = error`` によって異常終了となります。

JSONフィールドの設定
====================

Direct I/O JSON が扱うテキストファイルのJSONフィールドに関する設定は、DMDLスクリプトのデータモデルに含まれるそれぞれのプロパティに ``@directio.json.field`` 属性を指定します。

``@directio.json.field`` 属性の要素には、次のような設定を指定することができます。

* `フィールドの基本情報`_
* `フィールドのデータフォーマット`_

その他、JSONフィールドに対する個別の属性を利用した、次のような設定を指定することができます。

* `フィールドの除外`_
* `ファイル情報の取得`_

以下はDMDLスクリプトの記述例です。

..  code-block:: dmdl

    @directio.json (
        ...
    )
    model = {
        @directio.json.field (
            name = "total_amount",
            null_style = absent,
            decimal_output_style = plain,
        )
        amount : DECIMAL;
    };

フィールドの基本情報
--------------------

``name``
  JSONフィールド名を表す文字列。

  この値とJSONキー文字列が一致するJSONフィールドが、この属性を指定したプロパティの入出力先となる。

  既定値: 未指定

フィールドのデータフォーマット
------------------------------

`データフォーマットの設定`_ が持つ設定のうち、次の項目については ``@directio.json.field`` 属性に同名の要素を指定することでJSONフィールド単位に設定を上書きすることができます。

* `データ型の形式`_

  * ``date_format``
  * ``datetime_format``
  * ``null_style``
* `入力時の動作`_

  * ``on_malformed_input``
  * ``on_missing_input``

フィールドの除外
----------------

データモデルに定義されている特定のプロパティをJSONフィールドとして取り扱いたくない場合の設定です。

``@directio.json.ignore``
  このプロパティをJSONフィールドとして取り扱わない。

ファイル情報の取得
------------------

入力時のテキストファイルに関する情報を取得する場合、それぞれ次の属性をプロパティに指定します。

これらの属性はファイル入力時のみ有効です。
これらの属性を指定したプロパティは、ファイル出力時にはJSONフィールドから除外されます。

``@directio.json.file_name``
  このフィールドに、該当データレコードが含まれるファイルパスを設定する。

  この属性を指定するプロパティには ``TEXT`` 型を指定する必要がある。

``@directio.json.line_number``
  このフィールドに、該当データレコードの開始行番号（テキスト行番号）を設定する。

  この属性を指定するプロパティには ``INT`` または ``LONG`` 型を指定する必要がある。

  この属性が指定された場合、 :ref:`directio-input-split` が行われなくなる。

``@directio.json.record_number``
  このフィールドに、該当データレコードのレコード番号を設定する。

  この属性を指定するプロパティには ``INT`` または ``LONG`` 型を指定する必要がある。

  この属性が指定された場合、 :ref:`directio-input-split` が行われなくなる。

制限事項
========

Asakusa Framework バージョン |version| の Direct I/O JSON には、以下のような制限事項があります。

未対応のデータ型
----------------

Direct I/O JSON ではJSONの以下のデータ型を取り扱うことはできません。

* 配列
* オブジェクト

入力となるJSONのフィールドにこれらのデータ型が含まれていた場合、不正な値が検出された場合と同じ動作となります。
デフォルトの設定ではエラーとして異常終了しますが、 `データフォーマットの設定`_ の ``on_malformed_input`` または ``on_unknown_input`` を適切に設定することにより、
JSONファイル全体、またはJSONフィールド単位でこの動作を変更することもできます。
