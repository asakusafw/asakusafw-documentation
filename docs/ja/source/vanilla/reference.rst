============================
Asakusa Vanilla リファレンス
============================

この文書では、Asakusa Vanilla が提供するGradle PluginやDSLコンパイラの設定、およびバッチアプリケーション実行時の設定などについて説明します。

Asakusa Vanilla Gradle Plugin リファレンス
==========================================

Asakusa Vanilla Gradle Pluginが提供する機能とインターフェースについて個々に解説します。

プラグイン
----------

``asakusafw-vanilla``
    アプリケーションプロジェクトで、Asakusa Vanillaのさまざまな機能を有効にする。

    このプラグインは ``asakusafw-sdk`` プラグインや ``asakusafw-organizer`` プラグインを拡張するように作られているため、それぞれのプラグインも併せて有効にする必要がある（ ``apply plugin: 'asakusafw-vanilla'`` だけではほとんどの機能を利用できません）。

タスク
------

``vanillaCompileBatchapps``
    DSL Compiler for Vanillaを利用してDSLをコンパイルする [#]_ 。

    ``asakusafw-sdk`` プラグインが有効である場合にのみ利用可能。

``attachComponentVanilla``
    デプロイメントアーカイブにAsakusa Vanilla向けのバッチアプリケーションを実行するためのコンポーネントを追加する。

    ``asakusafw-organizer`` プラグインが有効である場合にのみ利用可能。

    ``asakusafwOrganizer.vanilla.enabled`` に ``true`` が指定されている場合、自動的に有効になる。

``attachVanillaBatchapps``
    デプロイメントアーカイブに ``vanillaCompileBatchapps`` でコンパイルした結果を含める。

    ``asakusafw-sdk`` , ``asakusafw-organizer`` の両プラグインがいずれも有効である場合にのみ利用可能。

    ``asakusafwOrganizer.batchapps.enabled`` に ``true`` が指定されている場合、自動的に有効になる。

..  [#] :asakusa-gradle-groovydoc:`com.asakusafw.gradle.tasks.AsakusaCompileTask`

タスク拡張
----------

``assemble``
    デプロイメントアーカイブを生成する。

    ``asakusafw-vanilla`` と ``asakusafw-organizer`` プラグインがいずれも有効である場合、 ``vanillaCompileBatchapps`` が依存関係に追加される。

``compileBatchapp``
    Asakusa DSLコンパイラを使ってバッチアプリケーションのコンパイルを行い、実行可能モジュールを生成する。

    ``asakusafw-vanilla`` プラグインが有効である場合、 ``vanillaCompileBatchapps`` が依存関係に追加される。

``jarBatchapp``
    ``compileBatchapp`` タスクで生成したバッチアプリケーションを含むjarファイルを生成する。

    ``asakusafw-vanilla`` プラグインが有効である場合、 ``vanillaCompileBatchapps`` タスクの生成物がjarファイルの内容に追加される。

規約プロパティ拡張
------------------

.. _vanilla-batch-application-plugin-ext:

Batch Application Plugin ( ``asakusafw`` ) への拡張
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Vanilla Gradle PluginはBatch Application Pluginに対してAsakusa Vanillaのビルド設定を行うための規約プロパティを追加します。この規約プロパティは、 ``asakusafw`` ブロック内の参照名 ``vanilla`` でアクセスできます。

以下、 ``build.gradle`` の設定例です。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-vanilla-reference-1

    asakusafw {
        vanilla {
            include 'com.example.batch.*'
        }
    }

この規約オブジェクトは以下のプロパティを持ちます。

``vanilla.version``
    Asakusa Vanilla のコンポーネントバージョンを保持する。

    この値は設定による変更は不可。

    既定値: Asakusa Vanilla Gradle Pluginが保持する既定のバージョン

``vanilla.outputDirectory``
    コンパイラの出力先を指定する。

    文字列や ``java.io.File`` などで指定し、相対パスが指定された場合にはプロジェクトからの相対パスとして取り扱う。

    既定値: ``"$buildDir/vanilla-batchapps"``

``vanilla.include``
    コンパイルの対象に含めるバッチクラス名のパターンを指定する。

    バッチクラス名には ``*`` でワイルドカードを含めることが可能。

    また、バッチクラス名のリストを指定した場合、それらのパターンのいずれかにマッチしたバッチクラスのみをコンパイルの対象に含める。

    既定値: ``null`` (すべて)

``vanilla.exclude``
    コンパイルの対象から除外するバッチクラス名のパターンを指定する。

    バッチクラス名には ``*`` でワイルドカードを含めることが可能。

    また、バッチクラス名のリストを指定した場合、それらのパターンのいずれかにマッチしたバッチクラスをコンパイルの対象から除外する。

    ``include`` と ``exclude`` がいずれも指定された場合、 ``exclude`` のパターンを優先して取り扱う。

    既定値: ``null`` (除外しない)

``vanilla.runtimeWorkingDirectory``
    実行時のテンポラリワーキングディレクトリのパスを指定する。

    パスにはURIやカレントワーキングディレクトリからの相対パスを指定可能。

    未指定の場合、コンパイラの標準設定である「 ``target/hadoopwork`` 」を利用する。

    既定値: ``null`` (コンパイラの標準設定を利用する)

``vanilla.option``
    `コンパイラプロパティ`_ （コンパイラのオプション設定）を追加する。

    後述する `コンパイラプロパティ`_ を ``<key>, <value>`` の形式で指定する [#]_ 。

    既定値: (Asakusa Vanilla向けのコンパイルに必要な最低限のもの)

``vanilla.batchIdPrefix``
    Asakusa Vanilla向けのバッチアプリケーションに付与するバッチIDの接頭辞を指定する。

    文字列を設定すると、それぞれのバッチアプリケーションは「 ``<接頭辞><本来のバッチID>`` 」というバッチIDに強制的に変更される。

    空文字や ``null`` を指定した場合、本来のバッチIDをそのまま利用するが、他のコンパイラが生成したバッチアプリケーションと同じバッチIDのバッチアプリケーションを生成した場合、アプリケーションが正しく動作しなくなる。

    既定値: ``"vanilla."``

``vanilla.failOnError``
    Asakusa Vanilla向けのコンパイルを行う際に、コンパイルエラーが発生したら即座にコンパイルを停止するかどうかを選択する。

    コンパイルエラーが発生した際に、 ``true`` を指定した場合にはコンパイルをすぐに停止し、 ``false`` を指定した場合には最後までコンパイルを実施する。

    既定値: ``true`` (即座にコンパイルを停止する)

..  [#] コンパイラプロパティを指定する方法は他にいくつかの方法があります。詳しくは :asakusa-gradle-groovydoc:`com.asakusafw.gradle.plugins.AsakusafwCompilerExtension` のメソッドの説明を参照してください。

.. _vanilla-framework-organizer-plugin-ext:

Framework Organizer Plugin ( ``asakusafwOrganizer`` ) への拡張
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asakusa Vanilla Gradle Plugin は Framework Organizer Plugin に対してAsakusa Vanillaのビルド設定を行うための規約プロパティを追加します。この規約プロパティは、 ``asakusafwOrganizer`` ブロック内の参照名 ``vanilla`` でアクセスできます。

この規約オブジェクトは以下のプロパティを持ちます。

``vanilla.enabled``
    デプロイメントアーカイブにAsakusa Vanillaのコンポーネント群を追加するかどうかを指定する。

    ``true`` を指定した場合にはコンポーネントを追加し、 ``false`` を指定した場合には追加しない。

    既定値: ``true`` (コンポーネント群を追加する)

``<profile>.vanilla.enabled``
    対象のプロファイルに対し、デプロイメントアーカイブにAsakusa Vanillaのコンポーネントを追加するかどうかを指定する。

    前述の ``vanilla.enabled`` と同様だが、こちらはプロファイルごとに指定できる。

    既定値: ``asakusafwOrganizer.vanilla.enabled`` (全体のデフォルト値を利用する)

コマンドラインオプション
------------------------

:program:`vanillaCompileBatchapps` タスクを指定して :program:`gradlew` コマンドを実行する際に、 ``vanillaCompileBatchapps --update <バッチクラス名>`` と指定することで、指定したバッチクラス名のみをバッチコンパイルすることができます。

また、バッチクラス名の文字列には ``*`` をワイルドカードとして使用することもできます。

以下の例では、パッケージ名に ``com.example.target.batch`` を含むバッチクラスのみをバッチコンパイルしてデプロイメントアーカイブを作成しています。

..  code-block:: sh

    ./gradlew vanillaCompileBatchapps --update com.example.target.batch.* assemble

そのほか、 :program:`vanillaCompileBatchapps` タスクは :program:`gradlew` コマンド実行時に以下のコマンドライン引数を指定することができます。

..  program:: vanillaCompileBatchapps

..  option:: --options <k1=v1[,k2=v2[,...]]>

    追加のコンパイラプロパティを指定する。

    規約プロパティ ``asakusafw.vanilla.option`` で設定したものと同じキーを指定した場合、それらを上書きする。

..  option:: --batch-id-prefix <prefix.>

    生成するバッチアプリケーションに、指定のバッチID接頭辞を付与する。

    規約プロパティ ``asakusafw.vanilla.batchIdPrefix`` の設定を上書きする。

..  option:: --fail-on-error <"true"|"false">

    コンパイルエラー発生時に即座にコンパイル処理を停止するかどうか。

    規約プロパティ ``asakusafw.vanilla.failOnError`` の設定を上書きする。

..  option:: --update <batch-class-name-pattern>

    指定のバッチクラスだけをコンパイルする (指定したもの以外はそのまま残る)。

    規約プロパティ ``asakusafw.vanilla.{in,ex}clude`` と同様にワイルドカードを利用可能。

    このオプションが設定された場合、規約プロパティ ``asakusafw.vanilla.{in,ex}clude`` の設定は無視する。

.. _vanilla-dsl-compiler-reference:

DSL Compiler for Vanilla リファレンス
=====================================

コンパイラプロパティ
--------------------

DSL Compiler for Vanillaで利用可能なコンパイラプロパティについて説明します。
これらの設定方法については、 `Batch Application Plugin ( asakusafw ) への拡張`_ の ``vanilla.option`` の項を参照してください。

``directio.input.filter.enabled``
    Direct I/O input filterを有効にするかどうか。

    ``true`` ならば有効にし、 ``false`` ならば無効にする。

    既定値: ``true``

``operator.checkpoint.remove``
    DSLで指定した ``@Checkpoint`` 演算子をすべて除去するかどうか。

    ``true`` ならば除去し、 ``false`` ならば除去しない。

    既定値: ``false``

``operator.logging.level``
    DSLで指定した ``@Logging`` 演算子のうち、どのレベル以上を表示するか。

    ``debug`` , ``info`` , ``warn`` , ``error`` のいずれかを指定する。

    既定値: ``info``

``operator.aggregation.default``
    DSLで指定した ``@Summarize`` , ``@Fold`` 演算子の ``partialAggregate`` に ``PartialAggregation.DEFAULT`` が指定された場合に、どのように集約を行うか。

    ``total`` であれば部分集約を許さず、 ``partial`` であれば部分集約を行う。

    既定値: ``total``

``input.estimator.tiny``
    インポーター記述の ``getDataSize()`` に ``DataSize.TINY`` が指定された際、それを何バイトのデータとして見積もるか。

    値にはバイト数か、 ``+Inf`` (無限大)、 ``NaN`` (不明) のいずれかを指定する。

    主に、 ``@MasterJoin`` 系の演算子でJOINのアルゴリズムを決める際など、データサイズによる最適化の情報として利用される。

    既定値: ``10485760`` (10MB)

``input.estimator.small``
    インポーター記述の ``getDataSize()`` に ``DataSize.SMALL`` が指定された際、それを何バイトのデータとして見積もるか。

    その他については ``input.estimator.tiny`` と同様。

    既定値: ``209715200`` (200MB)

``input.estimator.large``
    インポーター記述の ``getDataSize()`` に ``DataSize.LARGE`` が指定された際、それを何バイトのデータとして見積もるか。

    その他については ``input.estimator.tiny`` と同様。

    既定値: ``+Inf`` (無限大)

``operator.join.broadcast.limit``
    ``@MasterJoin`` 系の演算子で、broadcast joinアルゴリズムを利用して結合を行うための、マスタ側の最大入力データサイズ。

    基本的には ``input.estimator.tiny`` で指定した値の2倍程度にしておくのがよい。

    既定値: ``20971520`` (20MB)

``operator.estimator.<演算子注釈名>``
    指定した演算子の入力に対する出力データサイズの割合。

    「演算子注釈名」には演算子注釈の単純名 ( ``Extract`` , ``Fold`` など) を指定し、値には割合 ( ``1.0`` , ``2.5`` など) を指定する。

    たとえば、「 ``operator.estimator.CoGroup`` 」に ``5.0`` を指定した場合、すべての ``@CoGroup`` 演算子の出力データサイズは、入力データサイズの合計の5倍として見積もられる。

    既定値: `operator.estimator.* のデフォルト値`_ を参照

``<バッチID>:<オプション名>``
    指定のオプションを、指定のIDのバッチに対してのみ有効にする。

    バッチIDは ``vanilla.`` などのプレフィックスが付与する **まえの** ものを指定する必要がある。

    既定値: N/A

``dag.planning.option.unifySubplanIo``
    等価なステージの入出力を一つにまとめる最適化を有効にするかどうか。

    ``true`` ならば有効にし、 ``false`` ならば無効にする。

    無効化した場合、ステージの入出力データが増大する場合があるため、特別な理由がなければ有効にするのがよい。

    既定値: ``true``

``dag.planning.option.checkpointAfterExternalInputs``
    ジョブフローの入力の直後にチェックポイント処理を行うかどうか。

    ``true`` ならばチェックポイント処理を行い、 ``false`` ならば行わない。

    既定値: ``false``

operator.estimator.* のデフォルト値
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  list-table:: operator.estimator.* のデフォルト値
    :widths: 3 7
    :header-rows: 1

    * - 演算子注釈名
      - 計算式
    * - ``Checkpoint``
      - 入力の ``1.0`` 倍
    * - ``Logging``
      - 入力の ``1.0`` 倍
    * - ``Branch``
      - 入力の ``1.0`` 倍
    * - ``Project``
      - 入力の ``1.0`` 倍
    * - ``Extend``
      - 入力の ``1.25`` 倍
    * - ``Restructure``
      - 入力の ``1.25`` 倍
    * - ``Split``
      - 入力の ``1.0`` 倍
    * - ``Update``
      - 入力の ``2.0`` 倍
    * - ``Convert``
      - 入力の ``2.0`` 倍
    * - ``Summarize``
      - 入力の ``1.0`` 倍
    * - ``Fold``
      - 入力の ``1.0`` 倍
    * - ``MasterJoin``
      - トランザクション入力の ``2.0`` 倍
    * - ``MasterJoinUpdate``
      - トランザクション入力の ``2.0`` 倍
    * - ``MasterCheck``
      - トランザクション入力の ``1.0`` 倍
    * - ``MasterBranch``
      - トランザクション入力の ``1.0`` 倍
    * - ``Extract``
      - 既定値無し
    * - ``GroupSort``
      - 既定値無し
    * - ``CoGroup``
      - 既定値無し

既定値がない演算子に対しては、有効なデータサイズの見積もりを行いません。

実行時の設定
============

Asakusa Vanillaのバッチアプリケーション実行時の設定は、 `設定ファイル`_ を使う方法と `環境変数`_ を使う方法があります。

設定ファイル
------------

Asakusa Vanillaに関するバッチアプリケーション実行時のパラメータは、 :file:`$ASAKUSA_HOME/vanilla/conf/vanilla.properties` に記述します。
このファイルは、 :doc:`user-guide` - デプロイメントアーカイブの作成 の設定を行った状態でデプロイメントアーカイブを作成した場合にのみ含まれています。

このファイルに設定した内容はAsakusa Vanillaのバッチアプリケーションの設定として使用され、バッチアプリケーション実行時の動作に影響を与えます。

環境変数
--------

Asakusa Vanillaに関するバッチアプリケーション実行時のパラメータは、環境変数 ``ASAKUSA_VANILLA_ARGS`` に設定することもできます。

環境変数 ``ASAKUSA_VANILLA_ARGS`` の値には ``--engine-conf <key>=<value>`` という形式でパラメータを設定します。

設定ファイルと環境変数で同じプロパティが設定されていた場合、環境変数の設定値が利用されます。

.. _vanilla_optimization_properties:

設定項目
--------

Asakusa Vanillaのバッチアプリケーション実行時の設定項目は以下の通りです。

``com.asakusafw.vanilla.thread.max``
    タスクを実行するワーカースレッドの最大数を設定します。

    既定値: ``1``

``com.asakusafw.vanilla.partitions``
    scatter-gather操作(シャッフル操作)のパーティション数を設定します。

    既定値: (ワーカースレッドの最大数)

    ..  hint::
        Asakusa Vanillaの現在の実装では、パーティション数をワーカースレッド数よりも大きな値にするメリットはほとんどありません。

``com.asakusafw.vanilla.pool.size``
    エンジン内で利用可能な入出力バッファーの合計サイズを設定します。

    この値を超えるバッファーを利用しようとした場合、古いバッファーをファイルシステム上に書き出します。

    既定値: ``268435456`` ( ``256MB`` )

    ..  hint::
        Asakusa Vanillaでは上記のバッファーをJVMのヒープ外に確保します。
        そのため、Java VMの設定でヒープサイズの上限を指定しても、それとは **別に** バッファー用のメモリを消費します。

``com.asakusafw.vanilla.pool.swap``
    古いバッファーをファイルシステム上に待避する際のファイルシステムパスを設定します。

    指定したパスの配下に一時ディレクトリを作成し、そこにバッファーファイルを作成します。

    既定値: (システムの一時ディレクトリー)

``com.asakusafw.vanilla.pool.compression``
    古いバッファーをファイルシステム上に待避する際の、ファイルの圧縮形式を指定します。

    以下のいずれかの値を指定可能です。

    ``com.asakusafw.vanilla.core.io.BufferedByteChannelDecorator``
      ファイルを圧縮せず、入出力のバッファリングのみを行います。

    ``com.asakusafw.vanilla.core.io.NullByteChannelDecorator``
      ファイルを圧縮せず、入出力のバッファリングも行いません。

    ``com.asakusafw.vanilla.client.util.SnappyByteChannelDecorator``
      ファイルをSnappy形式で圧縮します。

    ``com.asakusafw.vanilla.client.util.Lz4ByteChannelDecorator``
      ファイルをLZ4形式で圧縮します。

      LZ4形式を利用する場合、LZ4ライブラリ `lz4-java`_ をVanilla実行環境のクラスパスに配置する必要があります。
      以下、`lz4-java`_ を含めたデプロイメントアーカイブを生成する ``build.gradle`` の設定例です。

      ..  code-block:: groovy
          :caption: build.gradle
          :name: build.gradle-vanilla-reference-2

          configurations {
              lz4
          }
          dependencies {
              lz4 group: 'org.lz4', name: 'lz4-java', version: '1.5.1'
          }
          asakusafwOrganizer {
              assembly.into('vanilla/lib') {
                  put configurations.lz4
              }
          }

    既定値: ``com.asakusafw.vanilla.core.io.BufferedByteChannelDecorator``

``com.asakusafw.vanilla.output.buffer.size``
    出力バッファーあたりのバイト数を設定します。

    各出力が、この値から後述の「出力バッファのマージン値」を引いた値( ``com.asakusafw.vanilla.output.buffer.size`` - ``com.asakusafw.vanilla.output.buffer.margin`` )を超えた場合、次のバッファーを新たに確保して出力を続行します。

    既定値: ``4194304`` ( ``4MB`` )

    ..  hint::
        古いバッファーをファイルシステム上に待避する際、各ファイルのサイズはおよそここで指定したサイズ以下になります。

``com.asakusafw.vanilla.output.buffer.margin``
    出力バッファーのマージンとなるバイト数を設定します。

    この値は実行時に取り扱う最大レコードサイズよりも大きな値を設定すべきです。

    また、この値は ``com.asakusafw.vanilla.output.buffer.size`` の1/2より小さい値を設定してください。
    最大レコードサイズが大きいことでこれが満たせない場合、 ``com.asakusafw.vanilla.output.buffer.size`` の値を調整してください。

    既定値: ``1048576`` ( ``1MB`` )

``com.asakusafw.vanilla.output.record.size``
    レコードサイズの推定平均バイト数を設定します。

    この値は、出力バッファー当たりの最大レコード数を算出するために利用します。

    既定値: ``64``

    ..  hint::
        この値を大きくしすぎると、出力バッファーサイズを大きくしてもバッファー当たりのレコード数がすぐに上限に達してしまい、バッファーを有効活用できなくなります。
        また、この値を小さくしすぎると、出力バッファーごとのレコード管理のためのメタデータが大きくなりすぎてしまいます。

        出力バッファーサイズに極端に大きな値を指定する場合や、消費メモリー量を細かく制御したい場合を除き、この設定を変更する必要はありません。

``com.asakusafw.vanilla.merge.threshold``
    各スレッド毎の、scatter-gather操作でマージ処理を行う際の入力チャンク数を指定します。

    入力チャンク数がこの値を超過する場合、この値と後述の ``com.asakusafw.vanilla.merge.factor`` の値に従い、入力チャンクに対して段階的にマージ処理を行います。

    既定値: ``0`` （段階的マージを無効とし、すべての入力チャンクを一度にマージする）

``com.asakusafw.vanilla.merge.factor``
    上記 ``com.asakusafw.vanilla.merge.threshold`` の設定に従って段階的マージを行う際に、マージ処理の対象となるファイル数を決定する係数を設定します。

    マージが実行される際には ``com.asakusafw.vanilla.merge.threshold`` * ``com.asakusafw.vanilla.merge.factor`` で算出されたファイル数を一度にマージします。

    既定値: ``0.75``

``com.asakusafw.dag.input.file.directory``
  :doc:`../dsl/operators` - :ref:`spill-input-buffer` などを利用してメモリ上のバッファをファイルとして退避する際に使用する、
  ファイルの出力先ディレクトリを設定します。

  既定値: なし (未指定の場合、JVMのシステムプロパティ ``java.io.tmpdir`` で設定されているディレクトリを利用)

  ..  attention::
      大量のバッファが出力されるような処理を実行する場合には、出力先に十分な空き領域を確保する必要があることに注意してください。

``hadoop.<name>``
    指定の ``<name>`` を名前に持つHadoopの設定を追加します。

    ..  hint::
        Asakusa Vanillaでは、一部の機能 (Direct I/Oなど) にHadoopのライブラリ群を利用しています。
        このライブラリ群がHadoopの設定を参照している場合、この項目を利用して設定値を変更できます。

        Asakusa全体に関するHadoopの設定は ``$ASAKUSA_HOME/core/conf/asakusa-resources.xml`` 内で行えますが、 同一の項目に対する設定が
        ``asakusa-resources.xml`` と ``hadoop.<name>`` の両方に存在する場合、後者の設定値を優先します。

..  _`lz4-java`: https://github.com/lz4/lz4-java

Java VMの設定
-------------

Asakusa Vanillaでバッチアプリケーションを実行する際には、Java VMをひとつ起動してそのプロセス内でAsakusaの演算子を実行します。

このとき、対象のJava VMを起動する際のオプション引数を、環境変数 ``ASAKUSA_VANILLA_OPTS`` で指定できます。

以下は環境変数の設定例です。

..  code-block:: sh

    export ASAKUSA_VANILLA_OPTS='-Xmx16g'

実行コマンドの設定
------------------

Asakusa Vanilla実行用のJVMプロセスを起動するJavaコマンドは、環境変数 ``JAVA_CMD`` で設定することができます。
``JAVA_CMD`` が未設定の場合、 ``PATH`` 環境変数に含まれる ``java`` コマンドが使用されます。

:ref:`vanilla-framework-organizer-plugin-ext` で ``vanilla.useSystemHadoop`` が ``true`` になっている場合、
Asakusa Vanilla実行用のJVMプロセスを起動するコマンドには ``hadoop`` コマンドが使用され、
このコマンドは環境変数 ``HADOOP_CMD`` で設定することができます。
``HADOOP_CMD`` が未設定の場合、 ``PATH`` 環境変数に含まれる ``hadoop`` コマンドが使用されます。

環境変数 ``ASAKUSA_VANILLA_LAUNCHER`` は実行コマンドの先頭に任意のコマンド文字列を追加します。

..  tip::
    バッチアプリケーション実行時の環境変数は、YAESSプロファイルで設定することも可能です。

    Asakusa Vanillaを利用する場合、コマンドラインジョブのプロファイル ``command.vanilla`` が利用できます。 :file:`$ASAKUSA_HOME/yaess/conf/yaess.properties` に ``command.vanilla.env.HADOOP_CMD`` といったような設定を追加することで、YAESSからAsakusa Vanillaを実行する際に環境変数が設定されます。

    YAESSのコマンドラインジョブの設定方法について詳しくは、 :doc:`../yaess/user-guide` - :ref:`yaess-profile-command-section` などを参照してください。


ログの設定
----------

Asakusa Vanillaの実行時のログ設定は、Logback設定ファイル ``$ASAKUSA_HOME/vanilla/conf/logback.xml`` で設定します。

WindGate JDBC ダイレクト・モード
================================

|M3BP_FEATURE| 向けの機能として提供しているWindGate JDBC ダイレクト・モードはAsakusa Vanillaからも利用することができます。

WindGate JDBC ダイレクト・モードを利用するには、アプリケーションプロジェクトのビルドスクリプト( ``build.gradle`` )にこのモードを利用するためのコンパイルオプションを指定します。

以下、 ``build.gradle`` の設定例です。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-vanilla-reference-3

    asakusafw {
        vanilla {
            option 'windgate.jdbc.direct', '*'
        }
    }

WindGate JDBC ダイレクト・モードの利用方法などについては、|M3BP_FEATURE| の以下のドキュメントを参照してください。

* :doc:`../m3bp/optimization` - :ref:`windgate-jdbc-direct-mode`
