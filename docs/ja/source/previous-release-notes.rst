====================
過去のリリースノート
====================

Asakusa Frameworkの過去バージョンのリリースノートです。

すべての変更点一覧は :doc:`changelogs` も参照してください。

Release 0.9.2
=============

Aug 07, 2017

`Asakusa Framework 0.9.2 documentation`_

..  _`Asakusa Framework 0.9.2 documentation`: https://docs.asakusafw.com/0.9.2/release/ja/html/index.html

新機能と主な変更点
------------------

DMDLプロパティ参照
~~~~~~~~~~~~~~~~~~

DMDLプロパティ参照は、DMDLのレコードモデルおよび射影モデルに対して、複数のプロパティを単一のコレクションとして利用する機能をを提供します。

これらは固定長のリスト ( ``java.util.List`` ) またはマップ ( ``java.util.Map`` ) として利用でき、それぞれの要素はデータモデル内に存在するプロパティの参照を表します。 つまり、データモデル中のプロパティの値を変更するとリストやマップの値も変化し、リストやマップに対して変更を行うと、対応するプロパティの値が変化します。

このプロパティ参照を上手に利用すると、データモデル内に存在する「プロパティの繰り返し」を容易に処理できるようになります。

詳しくは、以下のドキュメントを参照してください。

* :doc:`../dmdl/user-guide` - :ref:`dmdl-property-references`

WindGate JDBC ダイレクト・モード を正式機能としてリリース
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

バージョン 0.9.0 から試験的機能として公開していた :ref:`windgate-jdbc-direct-mode` を正式機能として公開しました。

WindGate JDBC ダイレクト・モードとは、WindGateを利用したバッチアプリケーションの実行時にデータフロー処理を行うプロセスの内部で直接
WindGate JDBCによるデータベースへのインポート処理とエクスポート処理を行うように動作する、 |M3BP_FEATURE| 固有の最適化設定です。

WindGate JDBC ダイレクト・モードを利用することで、通常のWindGateよりもバッチアプリケーション全体の実行時間が大きく短縮できる可能性があります。

詳しくは、以下のドキュメントを参照してください。

* :doc:`m3bp/optimization` - :ref:`windgate-jdbc-direct-mode`

WindGate - Oracleパーティションテーブルの並列読み出し
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WindGateの最適化オプションに、Oracleパーティションテーブルに対する並列読み出しを行うオプションが追加されました。

この機能は、 :ref:`windgate-jdbc-direct-mode` でのみ利用することができます。
この機能の設定方法などは、 :ref:`windgate-jdbc-direct-mode` のドキュメントを参照してください。

その他の変更点
--------------

* :doc:`spark/index` - Direct I/O のファイル出力処理中に処理が失敗しても正常終了として扱われることがある問題を修正
* :doc:`spark/index` - :ref:`summarize-operator` の 集約関数 ``max`` を適用するデータに ``null`` が含まれていても、エラーにならず正常終了として扱われることがある問題を修正
* :doc:`spark/optimization` に Direct I/Oの入力スプリットを結合するオプション ``spark.hadoop.com.asakusafw.bridge.directio.input.combine`` を追加
* :doc:`m3bp/optimization` に :ref:`spill-input-buffer` で使用するディレクトリを変更するオプション ``com.asakusafw.dag.input.file.directory`` を追加

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

Release 0.9.1
=============

Apr 26, 2017

`Asakusa Framework 0.9.1 documentation`_

..  _`Asakusa Framework 0.9.1 documentation`: https://docs.asakusafw.com/0.9.1/release/ja/html/index.html

新機能と主な変更点
------------------

Direct I/O formatted text
~~~~~~~~~~~~~~~~~~~~~~~~~

Direct I/Oでレコードやフィールドを区切り文字によって分割するデータ形式を取り扱うための機能 :doc:`../directio/formatted-text` を追加しました。

従来、Direct I/Oで提供していた :doc:`../directio/csv-format` や :doc:`../sandbox/directio-tsv` などのテキストフォーマットを扱う機能と比べて、以下のような特徴を持っています。

* 多様なデータ形式を扱うきめ細かな設定が可能

  * データ形式に関する様々な設定をレコード全体、及びフィールド単位にそれぞれ設定することができます。
  * 従来、事前にデータ整形処理が必要であったようなデータ形式の多くは、この機能で直接処理可能となります。
* 不整合データに対する柔軟な動作設定が可能

  * 不整合データの検出時にエラーとして異常終了、警告を出力して処理を継続、単にスキップするなど様々な動作設定が可能です。
  * 想定外のデータやアプリケーションの仕様変更などに対して柔軟な対応が可能となります。

詳しくは、以下のドキュメントを参照してください。

* :doc:`../directio/formatted-text`

Direct I/Oのデータフォーマットファイルをテストデータに指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct I/Oを利用したアプリケーションのテストでは通常のテスト方法に加えて、Direct I/Oのデータフォーマットに対応するファイルをテストデータとして指定することが可能になりました。

例えば、CSVやTSVファイルを演算子やデータフローのテストに対する入力データや期待値データとして指定することができます。

詳しくは、以下のドキュメントを参照してください。

* :doc:`../directio/user-guide` - :ref:`directio-testdriver-dataformat`

その他の変更点
--------------

* Direct I/O の :ref:`directio-output-filename-pattern` で利用可能なプレースホルダで数値書式の対応を追加
* :ref:`operator-testing-with-result` 向けのユーティリティメソッド ``OperatorTestEnvironment#newResult`` を追加
* :ref:`vup-gradle-wrapper` の手順で設定されるGradleラッパーの取得先URLをGradleの標準設定に合わせて ``http`` から ``https`` に変更
* :doc:`../m3bp/index` 標準の設定下で単一の入力グループが2GB以上になるとエラーが発生する制限事項を解消
* :doc:`../m3bp/index` 特定の条件でデータフローのコンパイルが正しく行われないことがある問題 [#]_ を修正
* :ref:`windgate-jdbc-direct-mode` 特定の条件でデッドロックが発生する問題を修正
* :doc:`sandbox/intellij-idea` (試験的機能) ドキュメントの追加、及び従来の利用手順(Gradle IDEA Plugin拡張の利用)を非推奨化
* :doc:`product/target-platform` のアップデート

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

..  [#] https://github.com/asakusafw/asakusafw-compiler/pull/119

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

Release 0.9.0
=============

Dec 05, 2016

`Asakusa Framework 0.9.0 documentation`_

..  _`Asakusa Framework 0.9.0 documentation`: https://docs.asakusafw.com/0.9.0/release/ja/html/index.html

はじめに
--------

今回のリリースよりAsakusa Frameworkのリリース方式を変更し、
Asakusa Frameworkのコアや拡張コンポーネント群をまとめた「ディストリビューション」形式でリリースを行います。

従来のリリース方式ではAsakusa Frameworkが提供する各コンポーネントは個別にリリースされていました。
このためアプリケーション開発者は利用するコンポーネントのバージョンを個別に把握して設定する必要がありました。
またこれにより、互換性がないコンポーネントバージョンを組み合わせて設定してしまう恐れがありました。

今回採用するディストリビューション形式のリリースにより、
Asakusa Frameworkが提供する様々なコンポーネントを単一のバージョンで利用可能にします。
ディストリビューションに含まれる各コンポーネントの組み合わせは互換性があることが保証されます。

今回のリリース以降、このドキュメントはディストリビューションのリリース単位で作成されます。
このドキュメントに記載するAsakusa Frameworkのバージョンは、特別な記載がない限りディストリビューションのバージョンを表します。

ディストリビューションに含まれる各コンポーネントとそのバージョンは :doc:`changelogs` に記載しています。

新機能と主な変更点
------------------

Asakusa Framework Core/SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Gradle Plugin - ディストリビューションプラグイン
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

「はじめに」で説明したディストリビューションを利用するために、
Asakusa Gradle Pluginに「ディストリビューションプラグイン」を追加しました。
Asakusa Framework 0.9.0 以降のプロジェクトテンプレートを利用する場合、標準でこのディストリビューションプラグインが使用されます。

バージョン 0.8系を利用しているプロジェクトからのマイグレーションについては、以下のドキュメントを参照してください。

* :doc:`application/gradle-plugin-v09-changes`

WindGate - データベース接続時の最適化オプション
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

WindGateのデータベースとの接続時に利用する最適化オプションを設定する機能が追加されました。
この機能は主にデータベース固有の最適化機能を利用するために使用することを想定しています。

Asakusa Framework 0.9.0 では Oracleのダイレクト・パス・インサートを利用するクエリーを発行するためのオプションが追加されています。

詳しくは、以下のドキュメントを参照してください。

* :doc:`windgate/user-guide` - :ref:`windgate-resource-jdbc-optimizations`

Direct I/O - CSVフィールドのクォート方式の指定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Direct I/O CSVでフィールド値の内容に関わらず、常にクォート処理を行うモードが追加されました。
また、CSVの各フィールドで個別にモードを指定するためのDMDL記述が追加されました。

Direct I/O CSVと連携するプロダクトでCSVフォーマットのクォートに関する制約がある場合に、この機能を利用することで連携時の問題を解消できる可能性があります。

詳しくは、以下のドキュメントを参照してください。

* :doc:`directio/csv-format` - :ref:`directio-csv-field-settings`

Asakusa on Spark
~~~~~~~~~~~~~~~~

Direct I/Oの出力処理をSpark上で実行
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

これまでのバージョンでは、Asakusa on Sparkを利用する場合でもDirect I/Oの出力処理はMapReduceジョブによって実行されていましたが、
本バージョンより、Direct I/Oの出力処理はSpark上で実行されるようになりました。

この改善により、Asakusa on Spark上でDirect I/Oを利用するバッチアプリケーションについては、Hadoop MapReduceを実行するための環境設定は不要になりました。
またMapReduceジョブの実行に必要なオーバーヘッドがなくなることで、バッチアプリケーションの実行性能が向上する可能性があります。

なお、この動作はコンパイラオプション ``spark.output.direct`` により変更可能です。詳しくは、以下のドキュメントを参照してください。

* :doc:`spark/reference`

またこの改善により、 :doc:`spark/iterative-extension` ではDirect I/Oの出力処理でも反復変数が利用可能になりました。

Spark 2.0に対応
^^^^^^^^^^^^^^^

本リリースより Spark 2.0 以降のバージョンに対応しました。

なお、本リリースより Spark 1.6 以前のバージョンは非対応になりました。

|M3BP_FEATURE|
~~~~~~~~~~~~~~~~

WindGate JDBC ダイレクト・モード (試験的機能)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

WindGate JDBC ダイレクト・モードとは、WindGateを利用したバッチアプリケーションの実行時にデータフロー処理を行うプロセスの内部で直接
WindGate JDBCによるデータベースへのインポート処理とエクスポート処理を行うように動作する、 |M3BP_FEATURE| 固有の最適化設定です。

WindGate JDBC ダイレクト・モードを利用することで、通常のWindGateよりもバッチアプリケーション全体の実行時間が大きく短縮できる可能性があります。

詳しくは、以下のドキュメントを参照してください。

* :doc:`m3bp/optimization` - :ref:`windgate-jdbc-direct-mode`

その他
~~~~~~

Asakusa Vanilla (試験的機能)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Asakusa Vanillaは、Asakusa Frameworkの内部機能として提供するDAG実行エンジン実装用のツールセットを使った、実行エンジンのリファレンス実装です。

Asakusa Vanillaは単一ノード上でアプリケーションを実行します。
軽量で比較的コンパイル速度が速く、実行時にJVM以外の環境を必要としない、といった特徴を持っています。
このため将来のバージョンでは、Asakusa Vanillaを :doc:`mapreduce/emulation-mode` で利用する標準の実行エンジンに採用することを計画しています。

詳しくは、以下のドキュメントを参照してください。

* :doc:`sandbox/asakusa-vanilla`

互換性に関して
--------------

対応プラットフォーム
~~~~~~~~~~~~~~~~~~~~

本リリースでは、対応プラットフォームに関する重要な変更と非互換性があります。

Java (JDK)
  Java7、およびJDK 7は非対応になりました。

  Java7、およびJDK 7を利用している場合、Java 8 (JDK 8)に移行する必要があります。

Spark
  Spark 1.6 以前のバージョンは非対応になりました。

  Spark 1.6、およびそれ以前のバージョンを利用している場合、Spark 2.0 以降のバージョンに移行する必要があります。

変更内容の詳細やマイグレーション手順については、以下のドキュメント説明しています。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

削除された機能
~~~~~~~~~~~~~~

本リリースより、以下の機能は削除されました。

* レガシーモジュール
* Asakusa Legacy Gradle Plugin
* YAESSログの可視化 ( ``summarizeYaessJob`` タスク )

Release 0.8.2
=============

Dec 05, 2016

`Asakusa Framework 0.8.2 documentation`_

..  _`Asakusa Framework 0.8.2 documentation`: https://docs.asakusafw.com/0.8.2/release/ja/html/index.html

このバージョンはバグフィックスのみを含むメンテナンスリリースです。

変更点の詳細は :doc:`changelogs` を参照してください。

Release 0.8.1
=============

Jul 25, 2016

`Asakusa Framework 0.8.1 documentation`_

..  _`Asakusa Framework 0.8.1 documentation`: https://docs.asakusafw.com/0.8.1/release/ja/html/index.html

新機能と主な変更点
------------------

Direct I/O 出力カウンターの改善
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct I/O の出力時に表示されるカウンターに、出力ポートごとの統計情報が表示されるようになりました。

..  code-block:: none

    com.asakusafw.directio.output.port.Statistics
      categorySummary.bytes=91
      categorySummary.files=1
      categorySummary.records=3
      errorRecord.bytes=432
      errorRecord.files=1
      errorRecord.records=3

Direct I/O line を正式機能としてリリース
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

バージョン 0.7.5 から試験的機能として公開していた :doc:`Direct I/O line <directio/directio-line>` を正式機能として公開しました。

Direct I/O line は任意のテキストファイルを行ごとに読み書きするための機能です。
Direct I/Oが対応していないファイルフォーマットの入出力や、入力ファイルの整形や形式変換、バリデーションチェックなどの事前処理などに利用することができます。

Direct I/O lineの詳細は、以下のドキュメントを参照してください。

* :doc:`directio/directio-line`

Asakusa Framework チュートリアル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Frameworkのサンプルアプリケーションを作成しながら、フレームワークの基本的な使い方や開発の流れを紹介するチュートリアルを公開しました。

* :basic-tutorial:`Asakusa Framework チュートリアル <index.html>`

その他の変更点
~~~~~~~~~~~~~~

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

非推奨機能
~~~~~~~~~~

以下の機能の利用が非推奨になりました。

* :ref:`gradle-plugin-v08-specify-asakusafw-version` ( ビルドスクリプトの設定 )

  * バージョン 0.8.0 より、Asakusa FrameworkバージョンはAsakusa Gradle Pluginのバージョンから自動的に設定される値を利用することを推奨しています。
  * 特にバージョン 0.7.6 以前に作成したプロジェクトから移行する場合は :doc:`application/migration-guide` を確認して、必要に応じてビルドスクリプトを修正してください。
* :doc:`application/yaess-log-visualization`

  * この機能はバージョン 0.6.2 から試験的機能として提供していましたが、MapReduce以外の実行プラットフォームでは適切な分析が行えないなどの問題があるため、本バージョンより非推奨となりました。

ライブラリの構成変更
~~~~~~~~~~~~~~~~~~~~

Direct I/O lineが含まれるSDKアーティファクトが変更になりました。
過去バージョンのDirect I/O lineを利用しているプロジェクトについては、:doc:`application/migration-guide` を確認してください。

将来のバージョンにおける非互換性を含む変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

将来のバージョンにおいて、以下のプロダクトバージョンを対応プラットフォームから除外することを計画しています。

* Java: JDK7（JDK8にのみ対応）

Release 0.8.0
=============

Apr 08, 2016

`Asakusa Framework 0.8.0 documentation`_

..  _`Asakusa Framework 0.8.0 documentation`: https://docs.asakusafw.com/0.8.0/release/ja/html/index.html

はじめに
--------

Asakusa Frameworkは優れた開発生産性、高いパフォーマンスを発揮するバッチアプリケーションの開発、実行基盤として様々な改善を続けています。

今回のリリースでは、 新しい実行基盤である |M3BP_FEATURE| の新規公開、昨年からDeveloper Previewとして公開していた Asakusa on Spark の正式公開など重要なアップデートが多数含まれています。

また今回のリリースでは、より優れたプラットフォームへの対応を積極的に行うために、いくつかの古いプラットフォームの対応を削除しています。

新機能と主な変更点
------------------

|M3BP_FEATURE|
~~~~~~~~~~~~~~

|M3BP_FEATURE| は、Asakusa DSLを始めとするAsakusa Frameworkの開発基盤を利用して作成したバッチアプリケーションに対して、 |M3BP_ENGINE| (https://github.com/fixstars/m3bp) を実行基盤として利用するための機能セットを提供します。

|M3BP_ENGINE| はDAG (Directed Acyclic Graph; 有向非循環グラフ) の形で表現されたタスクをマルチコア環境で効率よく処理するためのフレームワークで、以下のような特徴があります。

* 単一ノード上のマルチコア/マルチプロセッサ用に最適化
* 細粒度で動的なタスクスケジューリング
* ほぼすべてオンメモリで処理

上記のような特徴のため、 小規模〜中規模のデータを扱うバッチに対して、|M3BP_FEATURE| によって単一ノード上で高速に処理できるようになりました。

|M3BP_FEATURE| の詳細は、以下のドキュメントを参照してください。

* :doc:`../m3bp/index`

Asakusa on Spark
~~~~~~~~~~~~~~~~

2015年からDeveloper Previewとして公開していた Asakusa on Spark を正式機能として公開しました。

Asakusa on Sparkは、Asakusa DSLを始めとするAsakusa Frameworkの開発基盤を利用して作成したバッチアプリケーションに対して、Apache Spark (https://spark.apache.org) を実行基盤として利用するための機能セットを提供します。

特に中規模〜大規模のデータを扱うバッチに対して、Asakusa on Sparkは優れたパフォーマンスを発揮します。

Asakusa on Spark の詳細は、以下のドキュメントを参照してください。

* :doc:`../spark/index`

Asakusa on Spark Iterative Extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa on Spark の拡張機能「Iterative Extensions」を試験的機能として公開しました。

Iterative Extensionsは、あるバッチに対してバッチ引数の一部または全部を変えながら同じバッチを連続して実行するための機能です。

Iterative Extensionsを適用したバッチを「反復バッチ」と呼びます。
反復バッチは通常のバッチを連続して実行する場合と比べて、次の点で高速に実行できる可能性があります。

* 連続処理によるリソースの効率的な利用

 連続するバッチアプリケーションを1つのSparkアプリケーションとして実行するため、特にYARN上での実行においては、アプリケーションコンテナの初期化などの分散オーバーヘッドが極小化される、コンテナリソースをシンプルな設定で最大限に利用できる、などの利点があります。

* 差分処理による最適化

 反復バッチでは連続するバッチ間で再計算が不要な箇所は実行結果を再利用することがあるため、特に実行するバッチアプリケーション間での変更箇所が少ない場合には、バッチ間の差分処理による利点が大きくなります。

反復バッチは、日付範囲を指定した日次バッチの一括実行や、パラメータ・スイープによるシミュレーションといった用途に適しています。

Iterative Extensionsは、反復バッチを定義するためのAsakusa DSLの拡張構文、反復バッチを生成するするためのAsakusa DSLコンパイラの拡張、および反復バッチを実行するためのインターフェースや実行モジュールなどを提供します。

Asakusa on Spark Iterative Extensions の詳細は、以下のドキュメントを参照してください。

* :doc:`../spark/iterative-extension`

対応プラットフォームの更新
~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーションプロジェクトで使用するGradleの標準バージョンを2.12にアップデートしました。

その他、いくつかの動作検証プラットフォームを更新しています。
詳しくは、 以下のドキュメントを参照してください。

* :doc:`product/target-platform`

また冒頭で述べた通り、今回のリリースではいくつかの古いプラットフォームの対応を削除しています。

詳しくは後述の互換性に関する説明を参照してください。

Asakusa Gradle Pluginの改善
~~~~~~~~~~~~~~~~~~~~~~~~~~~

|M3BP_FEATURE| や Asakusa on Spark のリリースに伴い、Gradle Plugin上で複数の実行基盤を統一的な方法で扱うための改善や、ビルド設定をシンプルに管理するための改善などをおこないました。

Asakusa Gradle Pluginの変更点については、以下のドキュメントを参照してください。

* :doc:`application/gradle-plugin-v08-changes`

その他の変更点
~~~~~~~~~~~~~~

その他、細かな機能改善およびバグフィックスが含まれます。

すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

変更点
~~~~~~

本リリースでは、対応プラットフォームに関する重要な変更と非互換性があります。

..  warning::
    バージョン 0.8.0 は以前のバージョンからいくつかの重要な変更が行われました。
    過去のバージョンからのマイグレーションを検討する際には必ず以下の内容を確認してください。

Java (JDK)
  Java6、およびJDK 6は非対応になりました。

  Java6、およびJDK 6を利用している場合、Java 7(JDK 7)、またはJava 8 (JDK 8)に移行する必要があります。

Hadoop
  Hadoop1系は非対応となりました。

  開発環境にHadoop1系をインストールしている場合、Hadoop2系をインストールしてAsakusa FrameworkからはHadoop2系を利用するよう設定してください。

  運用環境でHadoop1系を利用している場合、Hadoop2系に移行する必要があります。

Gradle
  Gradleのバージョン1系は非対応になりました。

  また、Asakusa Gradle Pluginにいくつか仕様変更が行われ、一部のタスクの動作やビルドスクリプトの設定方法が変更されています。

Maven
  Mavenの利用は非対応になりました。

  Mavenを利用しているアプリケーションプロジェクトは、Gradleを利用するよう移行する必要があります。

Asakusa Framework
  Hadoop1系が非対応となったことにより、Asakusa Framwork バージョン 0.7.0 から導入された「Hadoopバージョン」が廃止になりました。

  Asakusa Framework 0.7系では、Asakusa Framworkのバージョンは ``<version>-hadoop1``, ``<version>-hadoop2`` のように、利用するHadoopのバージョンを持つバージョン体系を導入していました。

  本リリース以降は、Asakusa Frameworkのバージョンは単一のバージョン体系 ( 例えば本リリースのバージョンは ``0.8.0`` ) を使用します。

変更内容の詳細やマイグレーション手順については、以下のドキュメント説明しています。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

..  attention::
    過去のバージョンからのマイグレーション作業を行う場合、必ず :doc:`application/migration-guide` と :doc:`administration/migration-guide` を確認してください。

Release 0.7.6
=============

Dec 02, 2015

`Asakusa Framework 0.7.6 documentation`_

..  _`Asakusa Framework 0.7.6 documentation`: https://docs.asakusafw.com/0.7.6/release/ja/html/index.html

このバージョンはAsakusa DSLコンパイラの以下の問題に対応したメンテナンスリリースです。

* MasterJoin系演算子のマスタ側入力に、 ``DataSize.TINY`` を含む2つ以上の入力を指定した場合に正しく動作しない問題を修正

その他、軽微なバグフィックスやドキュメント修正を含みます。

Release 0.7.5
=============

Nov 19, 2015

`Asakusa Framework 0.7.5 documentation`_

..  _`Asakusa Framework 0.7.5 documentation`: https://docs.asakusafw.com/0.7.5/release/ja/html/index.html

新機能と主な変更点
------------------

Direct I/O line - 特定フォーマットに依存しないテキストファイルの入出力
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct I/Oで任意のテキストファイルを行ごとに読み書きするための機能 :doc:`Direct I/O line <../directio/directio-line>` を追加しました。

Direct I/O lineはファイル内の行文字列とデータモデル内の1つの文字列型プロパティをマッピングする機能のみを提供します。
行文字列の解析、生成などの処理はバッチアプリケーションの演算子として記述します。

Direct I/O lineは、以下のような用途に利用することを想定しています。

* Direct I/Oが対応していないファイルフォーマットの入出力

  * 例えば `JSON <https://json.org>`_ や `LTSV <http://ltsv.org>`_ といったフォーマットを扱う場合に、行文字列をパースする処理と組み合わせて利用します。
* 入力ファイルの整形や形式変換、バリデーションチェックなどの事前処理

  * 例えばCSVファイルの一部にDirect I/Oでは直接扱えないような形式が含まれる場合に、事前に形式の変換を行うといった用途で利用します。

Direct I/O lineの詳細は、以下のドキュメントを参照してください。

* :doc:`directio/directio-line`

GradleのDSLコンパイル時に対象のバッチアプリケーションを指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gradleから :program:`compileBatchapp` タスクを指定してバッチアプリケーションのDSLコンパイルを実行する際に、 ``compileBatchapp --update <バッチクラス名>`` と指定することで、指定したバッチクラス名のみをバッチコンパイルすることができるようになりました。

詳細は、以下のドキュメントを参照してください。

* :doc:`application/gradle-plugin` - :ref:`gradle-plugin-dslcompile-filter`

開発環境向けの英語メッセージリソースの追加とAPIリファレンスの英語化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa DSLコンパイラのメッセージなど、従来日本語メッセージのみ提供していた機能に対して英語メッセージリソースを追加しました。

また、多くのAPIリファレンスの記述を日本語から英語に変更しました。

将来のバージョンで、全てのAPIリファレンスの記述を英語に統一する予定です。
また、日本語によるAPIの説明は本ドキュメントに記述するよう統一する予定です。

サポートプラットフォームの更新
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーション開発開発の動作検証プラットフォームにJava8(JDK 8)を追加しました。

また、アプリケーションプロジェクトで使用するGradleの標準バージョンを2.8にアップデートしました。

その他、いくつかの動作検証プラットフォームを更新しています。
詳しくは、 以下のドキュメントを参照してください。

* :doc:`product/target-platform`

その他の変更点
~~~~~~~~~~~~~~

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

将来のバージョンにおいて、以下のプロダクトバージョンを対応プラットフォームから除外することを計画しています。

* Hadoop: Hadoop1系 (Hadoop2系にのみ対応)
* Gradle: Gradleのバージョン1.12以前 (Gradle 2.X以降にのみ対応)
* Java: JDK6 （JDK7以降にのみ対応)

..  seealso::
    Hadoopバージョンについての詳細は :doc:`administration/deployment-guide` を参照してください

Release 0.7.4
=============

Aug 11, 2015

`Asakusa Framework 0.7.4 documentation`_

..  _`Asakusa Framework 0.7.4 documentation`: https://docs.asakusafw.com/0.7.4/release/ja/html/index.html

新機能と主な変更点
------------------

YAESSコマンドオプションの追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

YAESSのバッチ実行用コマンドに以下のオプションを設定できるようになりました。

* 任意のプロファイルセット(構成ファイル)を指定 ( ``-D profile=<プロファイル名>`` )
* 実行時の環境変数を指定 ( ``-V key=value`` )

YAESSコマンドオプションの詳細は、以下のドキュメントを参照してください。

* :doc:`yaess/user-guide`

ParquetのDATE型に対応
~~~~~~~~~~~~~~~~~~~~~

Direct I/O HiveでParquetを利用する場合にHiveの ``DATE`` 型を利用できるようになりました。

なお、ParquetのDATE型をHiveから利用する場合、Hiveのバージョン 1.2 以上を利用する必要があります。

詳細は、以下のドキュメントを参照してください。

* :doc:`directio/using-hive`

サポートプラットフォームの更新
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

いくつかのプラットフォームの対応バージョンを更新しています。

* MapR 5.0.0
* Hortonworks Data Platform 2.3
* Apache Hive 1.2.1

また、いくつかのHadoopディストリビューションでJDK8上での動作検証を行いました。

なお、アプリケーションの開発環境でのJDK8の利用については、現時点では基本的な動作のみ検証しています。

詳しくは、 :doc:`product/target-platform` を参照してください。

その他の変更点
~~~~~~~~~~~~~~

* Asakusa Gradle PluginがGradle 2.4以降で正常に動作しない問題を修正しました。
* WindGate-SSHを異なるHadoopバージョン間の環境で利用した場合の動作を改善しました。
* Windows上でHadoop2系を使ったエミュレーションモードが動作しない問題を修正しました。

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

将来のバージョンにおいて、以下のプロダクトバージョンを対応プラットフォームから除外することを計画しています。

* Hadoop: Hadoop1系 (Hadoop2系にのみ対応)
* Gradle: Gradleのバージョン1.12以前 (Gradle 2.X以降にのみ対応)
* Java: JDK6 （JDK7以降にのみ対応)

..  seealso::
    Hadoopバージョンについての詳細は :doc:`administration/deployment-guide` を参照してください

Release 0.7.3
=============

Apr 22, 2015

`Asakusa Framework 0.7.3 documentation`_

..  _`Asakusa Framework 0.7.3 documentation`: https://docs.asakusafw.com/0.7.3/release/ja/html/index.html

新機能と主な変更点
------------------

Direct I/O 入力フィルター
~~~~~~~~~~~~~~~~~~~~~~~~~

Direct I/O を利用してファイルからデータを読み出す際に、ファイル単位やレコード単位で読み出すデータを制限する機能を追加。

入力フィルターを使うことで、従来のDirect I/Oの機能では記述しきれないような複雑な絞り込みを行えるようになります。
バッチの実行パラメータと組み合わせることで、処理対象のデータを動的に制限することも可能です。
また、フィルターによるデータの絞り込みをDSLコンパイラの最適化設定と組み合わせることで、アプリケーションの高速化が望めます。

Direct I/O 入力フィルターが提供する機能には以下のようなものがあります。

パスフィルターメソッド
  入力の候補となるファイルパスに対して、個別に処理を行うかを決定するフィルタールールを記述します。

データフィルターメソッド
  入力の候補となるデータモデルの内容に基づいて、個別に処理を行うかを決定するフィルタールールを記述します。

Direct I/O 入力フィルターについての詳細は、以下のドキュメントを参照してください。

* :doc:`directio/user-guide` - :ref:`directio-input-filter`

スモールジョブ実行エンジンの正式対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Framework バージョン 0.7.1 ( `Release 0.7.1`_ ) で試験的機能として追加されたスモールジョブ実行エンジンに正式に対応しました。

正式対応に伴い、 :doc:`mapreduce/emulation-mode` で利用するための設定方法が変更になっています。
従来の設定で利用している環境も当面は引き続き利用可能ですが、できるだけ新しい設定方法を利用するようにしてください。

サポートプラットフォームの更新
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

いくつかのプラットフォームの対応バージョンを更新しています。

* Apache Hadoop 2.6.0
* Apache Hive 1.1.0
* MapR 4.1.0

詳しくは、 :doc:`product/target-platform` を参照してください。

その他の変更点
~~~~~~~~~~~~~~

* WindGate/JDBCでTRUNCATE時のクエリーをジョブフロー単位で指定可能になりました。
* Direct I/O及びWindGateでCSVファイルの入力時にヘッダーの検証をスキップするオプションを追加しました。
* テストドライバーを利用したインテグレーションテスト用のAPIを追加しました。
* 多相データフロー向けのコア演算子用APIを拡張しました。
* ドキュメントの構成を改善しました。

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

Java SE Development Kit (JDK)
  本バージョンからJDK6の利用は非推奨となりました。
  開発環境、運用環境共にJDK7を利用してください。

  Asakusa Frameworkが動作検証を行なっているJavaのバージョンについては、 :doc:`product/target-platform` を参照してください。
  また、開発環境で利用するJavaについての詳細は、 :doc:`application/using-jdk` を参照してください。

  なお、将来のバージョンではJDK6の利用は非対応とすることを計画しています。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.7.2
=============

Jan 05, 2015

`Asakusa Framework 0.7.2 documentation`_

..  _`Asakusa Framework 0.7.2 documentation`: https://docs.asakusafw.com/0.7.2/release/ja/html/index.html

新機能と主な変更点
------------------

Windows上でのアプリケーション開発に対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーション開発環境の対応プラットフォームとしてWindowsを追加しました。

:doc:`introduction/start-guide-windows` ではWindows上にアプリケーション開発環境を構築し、サンプルアプリケーションを例に開発環境を利用する方法を紹介しています。

Windowsでは運用機能に制限がありますが、アプリケーションの開発、テスト、ビルド機能のほぼすべてを利用することができます。

Hive 0.14に対応
~~~~~~~~~~~~~~~

:doc:`Direct I/O Hive <directio/using-hive>` がHive 0.14.0に対応しました。

Direct I/O Hiveが出力するParquetフォーマットで ``TIMESTAMP`` や ``DECIMAL`` 型などHive 0.14で新たに対応したデータタイプを利用することができるようになりました。

その他の変更点
~~~~~~~~~~~~~~

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.7.1
=============

Nov 20, 2014

`Asakusa Framework 0.7.1 documentation`_

..  _`Asakusa Framework 0.7.1 documentation`: https://docs.asakusafw.com/0.7.1/release/ja/html/index.html

新機能と主な変更点
------------------

小さなデータの処理性能を改善 (Experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

10MB程度の非常に小さなデータを処理するステージについて、実行性能を向上させる「スモールジョブ実行エンジン」を追加しました。

バッチアプリケーション内に小さなデータを処理するステージが多数含まれる場合、この機能を有効にすると性能が改善する場合があります。

また、常に小さなデータを利用する開発環境上のテスト実行では、この機能と :doc:`エミュレーションモード <mapreduce/emulation-mode>` を組み合わせて利用することで、テストの実行時間を大幅に短縮できます。

運用環境で本機能を有効にするには、以下を参照してください。

* :doc:`mapreduce/configure-task-optimization`

開発環境で本機能を有効にするには、以下を参照してください。

* :doc:`mapreduce/emulation-mode`

サポートプラットフォームを追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

対応プラットフォームにHortonworks Data Platform 2.1を追加しました。

その他、いくつかのプラットフォームの対応バージョンを更新しています。

詳しくは、 :doc:`product/target-platform` を参照してください。

その他の変更点
~~~~~~~~~~~~~~

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.7.0
=============

Sep 25, 2014

`Asakusa Framework 0.7.0 documentation`_

..  _`Asakusa Framework 0.7.0 documentation`: https://docs.asakusafw.com/0.7.0/release/ja/html/index.html

新機能と主な変更点
------------------

Direct I/O Hive
~~~~~~~~~~~~~~~

`Apache Hive <https://hive.apache.org/>`_ で利用されるいくつかのファイルフォーマットをDirect I/Oで直接取り扱えるようになりました。
これにより、Apache Hiveのテーブルデータをアプリケーションから直接作成できるようになります。

本フィーチャーには主に以下の改善が含まれています。

Parquet / ORCFile フォーマット
  さまざまなクエリーエンジンがサポートしている、ParquetとORCFileフォーマットをDirect I/Oから読み書きできるようになりました。
DMDL上での各種フォーマットのサポート
  DMDLから各種Hive対応フォーマット向けのDataFormatクラスを自動生成できるようになりました。

  また、上記の方法で作成したデータモデルから、Hive Metastore向けにDDLスクリプトを自動生成できるようになりました。

Direct I/O Hiveについて詳しくは、以下のドキュメントを参照してください。

* :doc:`directio/using-hive`

Hadoop2系に正式対応
~~~~~~~~~~~~~~~~~~~

従来のHadoop1系に加え、以前のバージョンから試験的機能として対応していたHadoop2系に本バージョンから正式に対応しました。
これにより、最新のHadoopディストリビューション上でAsakusa Frameworkのアプリケーションを安全に実行できます。

なお、正式にサポートするHadoopのバージョンラインが複数になったことにより、Asakusa Frameworkのバージョン体系もそれに合わせて変化しています。詳しくは以下のドキュメントを参照してください。

* :doc:`application/migration-guide` - :ref:`v07-versioning-sysytem-changing`

本バージョンより、Gradleを利用したビルドシステムにおいて、開発環境や様々な運用環境で異なるHadoopのバージョンラインを使い分けられるようになりました。
利用方法については以下のドキュメントを参照してください。

* :doc:`application/gradle-plugin`
* :doc:`administration/deployment-guide`

テストドライバーの改善
~~~~~~~~~~~~~~~~~~~~~~

テストドライバーに以下の改善が加えられています。

Excelの数式をサポート
  Excelによるテストデータ定義において、セルに数式を指定できるようになりました。これにより、より柔軟な方法でテストデータの定義を行えるようになります。
いくつかの比較形式を追加
  Excelによるテストデータ定義において、誤差を許す比較や、大小比較をサポートしました。

  本機能を利用する場合、新しいバージョンのテストデータテンプレートが必要になります。Excelのテストデータテンプレートを再生成してください。
テストデータの事前検証
  テストデータやテスト条件に形式的な問題がある場合、Asakusa DSLのコンパイルやHadoop上での実行に先立ってエラーが報告されるようになりました。

Excelによるテストデータ定義に関して詳しくは、以下のドキュメントを参照してください。

* :doc:`testing/using-excel`

実行時パフォーマンスの改善
~~~~~~~~~~~~~~~~~~~~~~~~~~

以下の機能により、全体的なパフォーマンス改善が加えられています。

ライブラリファイルのキャッシュ
  フレームワークやアプリケーションのライブラリファイル群をHadoop上にキャッシュして再利用できるようになりました。
ステージ間の新しい中間データ形式
  中間データに独自の形式を利用するようになりました。また、中間データの入出力をマルチコアプロセッサー向けに改善しました。
Mapタスクのスケジューリングを改善
  Mapタスクの結合を行う遺伝的アルゴリズムを見直し、よりデータローカリティを重視するようになりました。

これらの機能に関する設定など詳しくは、以下のドキュメントを参照してください。

* :doc:`mapreduce/configure-library-cache`
* :doc:`mapreduce/configure-task-optimization`

----

| その他、 :doc:`product/target-platform` のアップデートや細かな機能改善およびバグフィックスが含まれます。
| すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

本リリースには、過去のリリースに対していくつかの潜在的な非互換性が存在します。

Java SE Development Kit (JDK)
  アプリケーションプロジェクトの標準設定で利用するJavaのバージョンをJDK 6からJDK 7に変更しました。

  Java 7に対応していないHadoopディストリビューション上でアプリケーションを実行する場合、手動でJDK 6に戻す必要があります。
Gradle
  Gradle 2.1に対応しました。

  以前のAsakusa FrameworkはGradle 2.0以降に対応していません。プロジェクトのAsakusa Frameworkのバージョンをダウングレードする場合に注意が必要です。
Maven
  本バージョンより非推奨となりました。当面は引き続き利用可能ですが、できるだけGradleを利用するようにしてください。

  マイグレーション手順については :doc:`application/gradle-plugin` - :ref:`migrate-from-maven-to-gradle` を参照してください。
Framework Organizer Plugin (Gradle)
  新機能の追加に伴い、いくつかのタスクが非推奨/利用不可能になりました。

  詳しくは、 :doc:`application/gradle-plugin-deprecated` を参照してください。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

..  warning::
    バージョン 0.7.0 は以前のバージョンからいくつかの重要な変更が行われました。
    過去のバージョンからのマイグレーションを検討する際には必ず :doc:`application/migration-guide` の内容を確認してください。

Release 0.6.2
=============

May 22, 2014

`Asakusa Framework 0.6.2 documentation`_

..  _`Asakusa Framework 0.6.2 documentation`: https://docs.asakusafw.com/0.6.2/release/ja/html/index.html

新機能と主な変更点
------------------

「小さなジョブ」の実行に関する最適化オプションの追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Frameworkのアプリケーション実行時における最適化設定として、以下のオプションを追加しました。

* Mapperごとにジョブの入力データサイズを判定し、データが小さい場合にMapperに対する入力スプリットを1つにまとめる: ``com.asakusafw.input.combine.tiny.limit``
* ジョブの入力データサイズを判定し、データが小さい場合に起動するReduceタスクを ``1`` に再設定する: ``com.asakusafw.reducer.tiny.limit``

実行するアプリケーションの特性に応じてこれらのオプションを有効にすることで、計算リソースの無駄遣いを抑制したり、タスク起動のオーバーヘッドを削減したりすることでアプリケーション実行時のパフォーマンスが向上する可能性があります。

詳しくは、 :doc:`administration/configure-hadoop-parameters` の上記設定項目の説明を参照してください。

対応プラットフォームのアップデート
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

動作検証プラットフォームのHadoopディストリビューションに CDH5 [#]_ を追加しました。
また、Amazon EMR [#]_ など一部のHadoopディストリビューションの動作検証バージョンをアップデートしました。

Hadoop2系での動作については、MRv2(YARN)上でアプリケーションを実行した際に不適切な最適化が適用されることによる性能上の問題や、MRv1上でアプリケーションが正常に実行されないことがある不具合などを修正し、安定性を向上させています。

アプリケーション開発環境については、Ubuntu Desktop 14.04 [#]_  や Gradle 1.12 [#]_ など動作検証プラットフォームのアップデートを行いました。

対応プラットフォームの一覧は、 :doc:`product/target-platform` を参照してください。

..  attention::
    本バージョンでは、Hadoop2系の対応は試験的機能として提供されます。
    Hadoop2系の利用について詳しくは :doc:`administration/deployment-hadoop2` を参照してください。

..  [#] https://www.cloudera.co.jp/products-services/cdh/cdh.html
..  [#] https://aws.amazon.com/jp/elasticmapreduce/
..  [#] https://www.ubuntu.com/desktop
..  [#] https://www.gradle.org/

YAESSログの可視化
~~~~~~~~~~~~~~~~~

試験的機能として、YAESSの実行時ログからCSV形式のレポートファイルを生成するYAESS Log Analyzerツール を追加しました。
アプリケーションの実行時間の分析などに有用です。

詳しくは、 :doc:`application/yaess-log-visualization` を参照してください。

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.6.1
=============

Mar 19, 2014

`Asakusa Framework 0.6.1 documentation`_

..  _`Asakusa Framework 0.6.1 documentation`: https://docs.asakusafw.com/0.6.1/release/ja/html/index.html

新機能と主な変更点
------------------

本リリースの新機能と主な変更点は以下の通りです。

* 以下の機能をSandboxから標準機能に昇格
   * テストドライバーのエミュレーションモード実行: :doc:`mapreduce/emulation-mode`
   * バッチテストランナーAPI: :doc:`testing/user-guide` - :ref:`testing-userguide-integration-test`
* Direct I/O の入力ファイルが存在しない場合にエラーとせず処理を続行するオプションを追加。
   * ``DirectFileInputDescription#isOptional()`` : :doc:`directio/user-guide`
* Asakusa Gradle Plugin が ThunderGate に対応、また内部動作と拡張性に関する多くの改善。

その他、細かな機能改善およびバグフィックスが含まれます。
すべての変更点は :doc:`changelogs` を参照してください。

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.6.0
=============

Feb 17, 2014

`Asakusa Framework 0.6.0 documentation`_

..  _`Asakusa Framework 0.6.0 documentation`: https://docs.asakusafw.com/0.6.0/release/ja/html/index.html

.. contents::
   :local:
   :depth: 2
   :backlinks: none

新機能と主な変更点
------------------

標準のビルドシステムをGradleに移行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

バッチアプリケーションの開発で使用する標準のビルドツールを従来のバージョンで使用していたMavenからGradleに移行しました。

バージョン ``0.5.2`` から試験的に提供していた :doc:`Asakusa Gradle Plugin <application/gradle-plugin>` に対して多くの改善とバグフィックスを行い、これを標準機能に昇格しました。
また、Asakusa Frameworkのドキュメント全体をGradleを利用した説明に変更しています。

Gradleを使ったアプリケーション開発の詳細や、Mavenを利用しているアプリケーションプロジェクトをGradleを利用したプロジェクトに移行する方法などについては以下のドキュメントを参照してください。

* :doc:`application/gradle-plugin`

Mavenの利用について
^^^^^^^^^^^^^^^^^^^

本バージョン、およびAsakusa Framework ``0.6`` 系ではMavenを使ったアプリケーションの開発もサポートしています。

Asakusa Framework ``0.7`` 系以降の将来のバージョンで、Mavenによるアプリケーション開発を非推奨とすることを検討しています。

Shafu - Gradleプロジェクト用Eclipse Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

標準のビルドシステムをGradleに移行したことにあわせて、Gradleを利用するアプリケーションプロジェクトの開発をサポートするEclipseプラグイン「Shafu (車夫)」を公開しました。

* :jinrikisha:`Shafu - Asakusa Gradle Plug-in Helper for Eclipse - <shafu.html>`

Shafu はバッチアプリケーション開発にGradleを利用する際に、Eclipseから透過的にビルドツール上の操作を行えます。
Shafu を使うことで、ターミナル上でのビルドツールの操作が不要となり、Eclipse上でアプリケーション開発に必要なほとんどの作業を行うことができるようになります。

テストドライバーにJavaオブジェクトによるテストデータ指定を追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テストドライバーに指定可能なテストデータの形式を従来のExcelとJson形式に加え、Javaオブジェクトの指定が可能になりました。

詳しくは、 :doc:`testing/user-guide` の「入力データと期待データをJavaで記述する」を参照してください。

アプリケーションビルド時のログを改善
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DMDLのコンパイルやAsakusa DSLのコンパイル、テストドライバーの実行時に出力されるログなどの出力内容を改善しました。

試験的機能(Sandbox)
--------------------

アプリケーションテスト用のエミュレーションモード
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

試験的機能として、アプリケーションテスト用のエミュレーションモードを公開しました。

エミュレーションモードでAsakusa DSLのテストを実行すると、Asakusa Frameworkが提供するラッパー機構を利用してHadoopの処理を実行します。

通常のテスト実行とは異なり、テストを実行しているプロセス内でほとんどの処理が行われるため、デバッグモードのブレークポイントなどを利用できるようになります。
また、カバレッジツールと連携して演算子メソッドのテストカバレッジを確認しやすくなります。

また、エミュレーションモードと連携したインテグレーションテスト用のツールとしてバッチテストランナーAPIを追加しました。

エミュレーションモードの詳細や利用方法などについては、以下のドキュメントを参照してください。

* :doc:`mapreduce/emulation-mode`

入力データサイズに応じて自動的にローカルモードでジョブを実行
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

試験的機能として、入力データサイズに応じて自動的にローカルモードでHadoopジョブを実行する実行時プラグインを公開しました。

このプラグインを利用することでバッチの実行にかかるHadoopのオーバーヘッドが適切に調整され、バッチ実行時間が改善する可能性があります。

現時点でこのプラグインは基本的な動作確認のみを行なっており、動作検証プラットフォームは Apache Hadoop 1.2.1 のみです。

利用方法は以下のREADMEを参照してください。

* https://github.com/asakusafw/asakusafw-sandbox/blob/0.6.0/asakusa-runtime-ext/README.md

互換性に関して
--------------

本リリースでは過去バージョンとの互換性に関する特別な情報はありません。

過去バージョンからのマイグレーション情報については、以下のドキュメントを参照してください。

* :doc:`application/migration-guide`
* :doc:`administration/migration-guide`

Release 0.5.3
=============

Dec 24, 2013

`Asakusa Framework 0.5.3 documentation`_

..  _`Asakusa Framework 0.5.3 documentation`: https://docs.asakusafw.com/0.5.3/release/ja/html/index.html

本リリースはAsakusa Frameworkの開発版リリースです。
主な変更内容は以下の通りです。

* Apache Hadoop 2.2.0 に試験的に対応

 * Hadoop2系の利用については、 :doc:`administration/deployment-hadoop2` を参照してください。

* JDK 7に対応

 * 開発環境におけるJDK 7の利用については、 `application/develop-with-jdk7` を参照してください。

* Hadoopディストリビューション、アプリケーション開発環境の動作検証プラットフォームをアップデート

 * :doc:`product/target-platform` を参照してください。

* DMDLコンパイラ, DSLコンパイラ, Direct I/O実行時のエラーメッセージを改善
* TestDriverのExcel 2007形式によるテストデータ定義に試験的に対応
* その他、多くの細かな機能改善、およびバグフィックス

Release 0.5.2
=============

Nov 20, 2013

`Asakusa Framework 0.5.2 documentation`_

..  _`Asakusa Framework 0.5.2 documentation`: https://docs.asakusafw.com/0.5.2/release/ja/html/index.html

本リリースはAsakusa Frameworkの開発版リリースです。
主な変更内容は以下の通りです。

* 試験的機能として、Gradleベースの新ビルドシステムを提供
   * 詳しくは、 :doc:`application/gradle-plugin` を参照してください。
* Direct I/O CSV, Direct I/O TSV(Sandbox) に入出力データの圧縮/解凍機能を追加
* その他、多くの細かな機能改善、およびバグフィックス。

Release 0.5.1
=============

Jul 26, 2013

`Asakusa Framework 0.5.1 documentation`_

..  _`Asakusa Framework 0.5.1 documentation`: https://docs.asakusafw.com/0.5.1/release/ja/html/index.html

本リリースはAsakusa Frameworkの開発版リリースです。
主な変更内容は以下の通りです。

* テストドライバーに演算子のトレースログを出力する機構を追加。
* アプリケーション依存ライブラリの管理方法を改善。
* DMDLコンパイラの日本語メッセージリソースを追加。
* その他、多くの細かな機能改善、およびバグフィックス。

Release 0.5.0
=============

May 9, 2013

`Asakusa Framework 0.5.0 documentation`_

..  _`Asakusa Framework 0.5.0 documentation`: https://docs.asakusafw.com/0.5.0/release/ja/html/index.html

本リリースはAsakusa Frameworkの開発版リリースです。
主な変更内容は以下の通りです。

* 試験的にCDH4に対応 [#]_ 。またいくつかの動作検証プラットフォームの追加。
* フレームワーク本体とバッチアプリケーションの構成情報を分離し、バッチアプリケーションの構成定義をシンプル化。
* 今後のAsakusa Frameworkの拡張のベースとなるFramework本体に対する多くのリファインメント。
* その他、多くの細かな機能改善、およびバグフィックス。

..  [#] CDH4上でAsakusa Frameworkを利用するためのドキュメントを、 Sandboxプロジェクトに公開しています。

* `Asakusa Framework Sandbox - CDH4上でAsakusa Frameworkを利用する`_

..  _`Asakusa Framework Sandbox - CDH4上でAsakusa Frameworkを利用する`: https://docs.asakusafw.com/sandbox/ja/html/administration/asakusa-on-cdh4.html

Release 0.4.0
=============

Aug 30, 2012

`Asakusa Framework 0.4.0 documentation`_

..  _`Asakusa Framework 0.4.0 documentation`: https://docs.asakusafw.com/0.4.0/release/ja/html/index.html

本リリースはAsakusa Frameworkの安定版リリースです。
主な変更内容は以下の通りです。

* [Direct I/O] ワイルドカード指定の出力機能などを追加し、試験的機能から正式機能として昇格。
* [Asakusa DSL] コンパイラ最適化のチューニングおよびバグフィックス。
* [YAESS] シミュレーションモードの実行やデプロイモジュールのバージョン検証機能などを追加。
* 動作検証プラットフォームの追加。
* 広範囲にわたるドキュメントの拡充と改善、および多くのドキュメントバグのフィックス。
* その他、多くの細かな機能改善、およびバグフィックス。

Release 0.2.6
=============

May 31, 2012

`Asakusa Framework 0.2.6 documentation`_

..  _`Asakusa Framework 0.2.6 documentation`: https://docs.asakusafw.com/0.2/release/ja/html/index.html

本リリースではYAESS マルチディスパッチ機能が追加されました。

これによりバッチやジョブフローなどを異なる複数のHadoopクラスターに振り分けて実行したり、それぞれ異なる設定で起動したりできるようになります。

* :doc:`yaess/multi-dispatch`

その他、多数の機能改善やバグフィックスが行われています。

Release 0.2.5
=============

Jan 31, 2012

本リリースでは試験的な機能として「Direct I/O」が追加されました。
これは、Hadoopクラスターから直接バッチの入出力データを読み書きするための機構です。

* :doc:`directio/index`

また、本バージョンでは対応プラットフォームの拡張として、従来のバージョンで対応していたHadoopディストリビューションであるCDH3に加えて、Apache Hadoop 0.20.203.0での動作検証が行われ、この環境で動作するための変更が行われています。

その他、細かな機能改善やバグフィックスが行われています。

Release 0.2.4
=============

Dec 19, 2011

本リリースからWindGateがGA (Generally Available) となりました。
WindGateにはローカルのCSVに対するデータ入出力を行う機能が追加となっています。

また、本リリースではドキュメントの構成を見直し、内容を大幅に拡充しました。
特に「Asakusa Framework入門」の追加、およびWindGateやYAESSに関する記述が多く追加されています。

* :doc:`introduction/index`

旧バージョンを使っている開発環境を0.2.4に移行するにはマイグレーション作業が必要となります。
詳しくは以下のマイグレーションガイドを参照してください。

* :doc:`application/migration-guide`

その他、細かな機能改善やバグフィックスが行われています。

Release 0.2.3
=============

Nov 16, 2011

本リリースでは、様々な環境に合わせて実行方法をカスタマイズすることが可能なバッチ実行ツール「YAESS」とThunderGateの差分インポート機能を実現する「ThunderGateキャッシュ」機能が追加されました。

* :doc:`yaess/index`
* :doc:`thundergate/cache`

今回のリリースでは、旧バージョンを使っている開発環境を0.2.3に移行するためにマイグレーション作業が必要となります。
詳しくは以下のマイグレーションガイドを参照してください。

* :doc:`application/migration-guide`

その他、細かな機能改善やバグフィックスが行われています。

Release 0.2.2
=============

Sep 29, 2011

本リリースではExperimental Featureとして「WindGate」が追加されました。

WindGateはThunderGateと同様にバッチに対するデータの外部入出力を行うモジュールですが、様々なプラットフォームに対応するよう設計され、ThunderGateに対してポータビリティが高いことが特徴です。

* :doc:`windgate/index`

その他、バグフィックスや細かい機能改善が行われています。

Release 0.2.1
=============

Jul 27, 2011

* Extract演算子の追加
* Restructure演算子の追加
* ThunderGateのCLOBサポート
* その他バグフィックス

Release 0.2.0
=============

Jun 29, 2011

* DMDLの導入
* テストドライバーの大幅な改善
* その他多くのバグフィックス

Release 0.1.0
=============
Mar 30, 2011

* 初版リリース

