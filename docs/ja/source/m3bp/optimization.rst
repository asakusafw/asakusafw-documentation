============================
|M3BP_FEATURE|\ の最適化設定
============================

この文書では、\ |M3BP_FEATURE|\ のバッチアプリケーション実行時の最適化設定について説明します。

設定方法
========

|M3BP_FEATURE|\ のバッチアプリケーション実行時の設定は、 `設定ファイル`_ を使う方法と `環境変数`_ を使う方法があります。

設定ファイル
------------

|M3BP_FEATURE|\ に関するバッチアプリケーション実行時のパラメータは、 :file:`$ASAKUSA_HOME/m3bp/conf/m3bp.properties` に記述します。
このファイルは、\ |M3BP_FEATURE| Gradle Pluginを有効にしてデプロイメントアーカイブを作成した場合にのみ含まれています。

このファイルに設定した内容は\ |M3BP_FEATURE|\ のバッチアプリケーションの設定として使用され、バッチアプリケーション実行時の動作に影響を与えます。

設定ファイルはJavaのプロパティファイルのフォーマットと同様です。以下は ``m3bp.properties`` の設定例です。

..  code-block:: properties
    :caption: m3bp.properties
    :name: m3bp.properties-optimization-1

    ## the max number of worker threads
    com.asakusafw.m3bp.thread.max=10

    ## the default number of partitions
    com.asakusafw.m3bp.partitions=10

.. _ASAKUSA_M3BP_ARGS:

環境変数
--------

|M3BP_FEATURE|\ に関するバッチアプリケーション実行時のパラメータは、環境変数 ``ASAKUSA_M3BP_ARGS`` に設定することもできます。

環境変数 ``ASAKUSA_M3BP_ARGS`` の値には ``--engine-conf <key>=<value>`` という形式でパラメータを設定します。

以下は環境変数の設定例です。

..  code-block:: sh

    export ASAKUSA_M3BP_ARGS='--engine-conf com.asakusafw.m3bp.thread.max=10'

設定ファイルと環境変数で同じプロパティが設定されていた場合、環境変数の設定値が利用されます。

..  hint::
    環境変数による設定は、バッチアプリケーションごとに設定を変更したい場合に便利です。

..  attention::
    :program:`yaess-batch.sh` などのYAESSコマンドを実行する環境と、\ |M3BP_FEATURE|\ を実行する環境が異なる場合（例えばYAESSのSSH機能を利用している場合）に、
    YAESSコマンドを実行する環境の環境変数が\ |M3BP_FEATURE|\ を実行する環境に受け渡されないことがある点に注意してください。

    YAESSではYAESSコマンドを実行する環境の環境変数をYAESSのジョブ実行先に受け渡すための機能がいくつか用意されているので、それらの機能を利用することを推奨します。
    詳しくは :doc:`../yaess/user-guide` などを参照してください。

.. _optimization_properties:

設定項目
========

|M3BP_FEATURE|\ のバッチアプリケーション実行時の設定項目は以下の通りです。

``com.asakusafw.m3bp.thread.max``
  タスクを実行するワーカースレッドの最大数を設定します。

  未設定の場合、利用可能な全てのCPUコアに対して一つずつワーカースレッドを割り当てます。

  既定値: (論理コア数)

  ..  hint::
      |M3BP_FEATURE|\ ではこの値をCPUコア数より極端に大きな値にすると性能が低下する場合があります。
      計算ノードのCPUを占有できる環境では既定値を利用し、そうでない場合には既定値よりも小さな値を設定するとよいでしょう。

      また、物理CPUコアに対して複数のスレッド(論理CPUコア)が存在する環境では、物理CPUコア数を設定した方が速くなるようなケースもあります。

``com.asakusafw.m3bp.thread.affinity``
  各ワーカースレッドへのCPUコアの割り当て方法を設定します。

  * ``none``

    * 特別な設定を行わず、OSによるCPUコアの割り当てを利用します

  * ``compact``

    * ワーカースレッドをCPUコアに割り当てる際に、同一ソケット上のコアから順番に割り当てていきます

  * ``scatter``

    * ワーカースレッドをCPUコアに割り当てる際に、異なるソケットのコアを順番に割り当てていきます

  既定値: ``none``

  ..  attention::
      この設定を有効(``none``\ 以外)にした場合、\ |M3BP_FEATURE|\ はハードウェアの情報を参照します。
      仮想環境などでCPUコアの情報を正しく取得できない場合にはあまり効果がありません。

      また、環境によっては\ ``none``\ 以外を指定した際にエラーとなる場合があります。

``com.asakusafw.m3bp.partitions``
  scatter-gather操作(シャッフル操作)のパーティション数を設定します。

  既定値: (論理コア数の8倍)

  ..  hint::
      この値はDAG上の各vertexの「タスク数」に大きな影響を与えます。
      基本的にscatter-gather操作の直後のvertexでは、パーティションごとにタスクが割り当てられて処理を行うため、上記パーティション数が少なすぎるとワーカースレッドに適切にタスクが行き渡りません。

      また、ワーカースレッド数と同程度のパーティション数を指定した場合、各パーティションの大きさに偏り (キーの偏り) があるとワーカースレッドへタスクを均等に割り当てられなくなります。

      多くの場合は、ワーカースレッド数の数倍を指定するのがよいでしょう。

``com.asakusafw.m3bp.output.buffer.size``
  個々の出力バッファのサイズをバイト数で設定します。

  既定値: ``4194304`` (``4MB``)

  ..  hint::
      このバッファサイズは大きくしすぎると余計にメモリを消費し、小さくしすぎるとバッファを書き出す回数が増えて性能が低下する場合があります。

``com.asakusafw.m3bp.output.buffer.records``
  個々の出力バッファの最大レコード数を設定します。

  既定値: ``524288``

  ..  hint::
      それぞれの出力バッファでは、ここで指定したレコード数が上限に達するか、または出力バッファの使用量がある閾値を超えるか、どちらかで出力バッファの内容を書き出しています。
      そのため、ここのレコード数を極端に小さな値に設定した場合、出力バッファに余裕があってもバッファの内容を頻繁に書き出してしまうことになります。

      また、上記レコード数に応じてレコードのメタ情報を保持するため、極端に大きな値を指定すると余計にメモリを消費することになります。

      個々のレコードが極端に小さかったり大きかったりすることが明らかな場合以外、この値を変更する必要はありません。

``com.asakusafw.m3bp.output.buffer.flush``
  個々の出力バッファの内容を書き出す際の閾値となる使用量の割合を指定します。

  この値には ``0.0`` から ``1.0`` までの値を指定できますが、実装によってはこれより狭い範囲の値に再設定される場合があります。

  既定値: ``0.8``

  ..  hint::
      それぞれの出力バッファでは、ここで指定したレコード数が上限に達するか、または出力バッファの使用量がある閾値を超えるか、どちらかで出力バッファの内容を書き出しています。
      そのため、ここの使用率の閾値に対して極端に小さな値に設定した場合、出力バッファに余裕があってもバッファの内容を頻繁に書き出してしまうことになります。

      また、それぞれのレコードの(シリアライズ後の)サイズは、「 ``バッファサイズ * (1.0 - 使用率の閾値)`` 」以下である必要があります。
      これを超えた場合、レコードがバッファに収まらなくなって正常に動作しない場合があります。

      個々のレコードが極端に小さかったり大きかったりすることが明らかな場合以外、この値を変更する必要はありません。

``com.asakusafw.m3bp.buffer.access``

  個々の入出力バッファのアクセス方式を設定します。

  * ``nio``

    * JavaのNIOを利用してバッファにアクセスします。

  * ``unsafe``

    * Javaの非推奨の方法を利用してバッファにアクセスします。

  既定値: ``nio`` (Java NIOを利用)

  ..  deprecated::
      Asakusa Framework 0.10.0 以降、 ``com.asakusafw.m3bp.buffer.access`` に ``unsafe`` を指定することは非推奨となりました。

``com.asakusafw.dag.input.file.directory``
  :doc:`../dsl/operators` - :ref:`spill-input-buffer` などを利用してメモリ上のバッファをファイルとして退避する際に使用する、
  ファイルの出力先ディレクトリを設定します。

  既定値: なし (未指定の場合、JVMのシステムプロパティ ``java.io.tmpdir`` で設定されているディレクトリを利用)

  ..  attention::
      大量のバッファが出力されるような処理を実行する場合には、出力先に十分な空き領域を確保する必要があることに注意してください。

``hadoop.<name>``
  指定の ``<name>`` を名前に持つHadoopの設定を追加します。

  |M3BP_FEATURE|\ では、一部の機能 (Direct I/Oなど) にHadoopのライブラリ群を利用しています。
  このライブラリ群がHadoopの設定を参照している場合、この項目を利用して設定値を変更できます。

  Asakusa全体に関するHadoopの設定は ``$ASAKUSA_HOME/core/conf/asakusa-resources.xml`` 内で行えますが、
  同一の項目に対する設定が ``asakusa-resources.xml`` と ``hadoop.<name>`` の両方に存在する場合、後者の設定値を優先します。

  ..  hint::
      |M3BP_FEATURE|\ に組み込まれたHadoopライブラリ群を利用する場合、システムにインストールされたHadoopの設定ファイルは利用されず、各Hadoopの既定値を利用します。
      このような場合、この設定項目を利用してHadoopの設定を上書きしてください。

      また、システムにインストールされたHadoopを利用する場合にも、\ |M3BP_FEATURE|\ 利用時のみ異なる設定を行うには、ここで指定するのがよいでしょう。

..  _windgate-jdbc-direct-mode:

WindGate JDBC ダイレクト・モード
================================

概要
----

WindGate JDBC ダイレクト・モードとは、:doc:`WindGate <../windgate/index>` を利用したバッチアプリケーションの実行時に
データフロー処理を行うプロセスの内部で直接WindGate JDBCによるデータベースへのインポート処理とエクスポート処理を行うように動作する最適化設定です。

通常のWindGateの動作は、バッチアプリケーションのメインとなるデータフローの処理の前後でそれぞれ
WindGateのプロセスを起動し、外部リソースからのデータの読み込み（インポート処理）と書き出し（エクスポート処理）を行います。

メインとなるデータフロー処理とWindGateの処理との間ではHadoopファイルシステムを介した中間データの受け渡しが必要になります。
また、インポート処理、データフロー処理、エクスポート処理はそれぞれのフェーズが完全に終了しないと次のフェーズに進むことができません。

これに対して「WindGate ダイレクト・モード」ではプロセス間の中間データの受け渡しは不要になり、フェーズ間の待ち合わせを設けないように設定することも可能です。
これらの動作により、通常のWindGateよりもバッチアプリケーション全体の実行時間が大きく短縮できる可能性があります。

WindGate JDBC ダイレクト・モードは |M3BP_FEATURE| でのみ利用可能です。

コンパイラの設定
----------------

WindGate JDBC ダイレクト・モードを利用するには、まずアプリケーションプロジェクトのビルドスクリプト( ``build.gradle`` )にこのモードを利用するためのコンパイルオプションを指定します。

以下、 ``build.gradle`` の設定例です。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-m3bp-optimization-1

    asakusafw {
        m3bp {
            option 'windgate.jdbc.direct', '*'
        }
    }

WindGate JDBC ダイレクト・モードに関するコンパイラオプションは以下の通りです。

``windgate.jdbc.direct``
    WindGate JDBC ダイレクト・モードを有効にするプロファイル名のパターン一覧を設定します。

    名前のパターンにはワイルドカードとして ``*`` を含めることができます。
    また、複数のパターンを指定する場合にはカンマ (``,``) 区切りで行います。

    コンパイル対象に、このパターンに適合するプロファイル名 [#]_ を持つWindGate JDBCの入出力 が含まれる場合、それらはWindGate JDBC ダイレクト・モード上で動作します。

    また、コンパイル対象に上記で指定した以外のプロファイル名を利用しているWindGate JDBCの入出力が含まれる場合、それらは従来のWindGate上で動作します。

    既定値: なし (利用しない)

``windgate.jdbc.direct.barrier``
    ``true`` を指定した場合、プロファイルごとに入力がすべて完了するまで出力の開始を遅延させます。
    ``false`` を指定した場合には、これを行いません。

    既定値: ``true`` (遅延させる)

    ..  warning::
        この設定に ``false`` を設定した場合、（グループ化やソートが含まれない）非常に単純なバッチが高速化されますが、特定の状況でデッドロックが発生する可能性があります。

        デッドロックを確実に回避するには、 `実行エンジンの設定`_ で「出力の最大並列実行数」よりも「最大同時接続数」を大きな値に設定する必要があります。

..  [#] バッチアプリケーションが利用するWindGateプロファイルの指定方法などについては、 :doc:`../windgate/user-guide` などを参照してください。

..  _windgate-jdbc-direct-mode-engine-conf:

JDBCドライバーの配置
--------------------

WindGate JDBC ダイレクト・モードで使用するJDBCドライバーのライブラリファイルは、 ``$ASAKUSA_HOME/m3bp/lib`` ディレクトリ直下に配置してください。

..  attention::
    通常のWindGateとJDBCドライバーファイルの配置ディレクトリが異なることに注意してください。

実行エンジンの設定
------------------

WindGate JDBC ダイレクト・モードに関する実行エンジンの設定は以下の通りです。
設定方法については上述の `設定方法`_ を参照してください。

..  attention::
    通常のWindGateはWindGateプロファイル上で動作設定を行いますが、WindGate JDBC ダイレクト・モードではこの設定を利用しません。
    |M3BP_FEATURE|\ の `設定方法`_ に従って本項で紹介する項目を設定してください。

``com.asakusafw.dag.jdbc.<profile-name>.url``
    対象のJDBC URLを指定します。

    既定値: なし (必須項目)

``com.asakusafw.dag.jdbc.<profile-name>.driver``
    対象のJDBCドライバークラス名を指定します。

    既定値: なし (必須項目)

``com.asakusafw.dag.jdbc.<profile-name>.properties.<key>``
    JDBC接続に対して、 ``<key>`` で指定した設定を追加します。

    ..  hint::
        多くのJDBCドライバーでは、 ``user`` と ``password`` の設定が必要です。

``com.asakusafw.dag.jdbc.<profile-name>.connection.max``
    最大同時接続数を設定します。

    既定値: `1`

    ..  hint::
        この接続数を超えて接続を試みた場合、他の接続が解放されるまで待ち合わせます。

``com.asakusafw.dag.jdbc.<profile-name>.input.records``
    JDBC経由でデータを取得する際に、一度に取得する最大行数を設定します。

    既定値: `1024`

``com.asakusafw.dag.jdbc.<profile-name>.output.records``
    JDBC経由でデータを出力する際に、一度にバッチ処理する最大行数を設定します。

    既定値: `1024`

``com.asakusafw.dag.jdbc.<profile-name>.input.threads``
    JDBC経由でデータを入力する際の、入力ごとの最大並列実行数を設定します。

    現在のバージョンでは、この設定は後述の ``com.asakusafw.dag.jdbc.<profile-name>.optimizations`` に ``ORACLE_PARTITION``
    を設定した場合に有効となる、Oracleのパーティションテーブルに対する並列読み込みを行うにのみ使用します。

    Oracleのパーティションテーブルに対する並列読み込みを有効にする場合、この設定値に `1` より大きな値を設定する必要があります。

    この設定は |M3BP_FEATURE|\ の「ワーカースレッドの最大数 (``com.asakusafw.m3bp.thread.max``)」以下である必要があります。

    既定値: `1`

    ..  hint::
        この値に最大同時接続数より大きな値を設定した場合、いくつかのスレッドは接続の取得を待ち合わせることになります。

``com.asakusafw.dag.jdbc.<profile-name>.output.threads``
    JDBC経由でデータを出力する際の、最大並列実行数を設定します。

    この設定は |M3BP_FEATURE|\ の「ワーカースレッドの最大数 (``com.asakusafw.m3bp.thread.max``)」以下である必要があります。

    既定値: `1`

    ..  hint::
        この値に最大同時接続数より大きな値を設定した場合、いくつかのスレッドは接続の取得を待ち合わせることになります。

``com.asakusafw.dag.jdbc.<profile-name>.output.clear``
    JDBC経由でデータを出力する際の、事前に出力先を削除する方式を設定します。

    利用可能な値:

    * ``delete`` - ``DELETE`` 文を利用してテーブルを削除します
    * ``truncate`` - ``TRUNCATE`` 文を利用してテーブルを削除します
    * ``keep`` - 削除を行いません

    既定値: ``truncate``

    ..  hint::
        この設定は、DSL側の ``JdbcExporterDescription.getCustomTruncate()`` で上書きできます。

``com.asakusafw.dag.jdbc.<profile-name>.optimizations``
    このプロファイルで利用可能な最適化項目の一覧を設定します。

    複数の項目を設定する場合、カンマ (``,``) 区切りで行います。

    利用可能な値:

    * ``ORACLE_DIRPATH`` - 出力時にOracleのダイレクトパス・インサートを有効にします
    * ``ORACLE_PARTITION`` - 入力時にOracleのパーティションテーブルに対する並列読み込みを有効にします。

    既定値: なし (有効にしない)

    ..  hint::
        この設定だけでは最適化が有効にならず、 ``Jdbc{Importer,Exporter}Description.getOptions()`` でも同名の項目を指定する必要があります。
        詳しくは :doc:`../windgate/user-guide` を参照してください。
