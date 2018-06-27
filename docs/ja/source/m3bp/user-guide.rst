==============================
|M3BP_FEATURE|\ ユーザーガイド
==============================

この文書では、\ |M3BP_FEATURE|\ を利用してバッチアプリケーションをビルドし、実行する方法について説明します。

概要
====

|M3BP_FEATURE|\ は、Asakusa DSLを始めとするAsakusa Frameworkの開発基盤を利用して作成したバッチアプリケーションに対して、\ |M3BP_ENGINE| [#]_ をその実行基盤として利用するための機能セットを提供します。

|M3BP_ENGINE|\ はDAG (Directed Acyclic Graph; 有向非循環グラフ) の形で表現されたタスクをマルチコア環境で効率よく処理するためのフレームワークで、以下のような特徴があります。

* 単一ノード上のマルチコア/マルチプロセッサ用に最適化
* 細粒度で動的なタスクスケジューリング
* ほぼすべてオンメモリで処理

上記のような特徴のため、Hadoop MapReduceやSparkに比べて、小〜中規模データサイズのバッチ処理に非常に適しています。

Asakusa Frameworkの適用領域においても、中間結果が全てメモリ上に収まる規模のバッチにおいてはAsakusa on Sparkよりも高速で、かつ高いコストパフォーマンスになることを確認しています [#]_ 。

.. [#] https://github.com/fixstars/m3bp
.. [#] http://www.asakusafw.com/techinfo/reference.html

構成
====

|M3BP_FEATURE|\ を利用する場合、従来のAsakusa Frameworkが提供するDSLやテスト機構をそのまま利用して開発を行います。
アプリケーションをビルドして運用環境向けの実行モジュール（デプロイメントアーカイブ）を作成する段階ではじめて\ |M3BP_FEATURE|\ のDSLコンパイラ(|M3BP_COMPILER|)を利用します。

..  figure:: attachment/asakusa-sdk.png
    :width: 640px

また、\ |M3BP_COMPILER|\ で生成したバッチアプリケーションは、従来と同様にYAESSを利用して実行できます。
このとき、MapReduceやSparkと異なり、実行基盤にHadoopを必要としません (`Hadoopとの連携`_\ により、HDFS等を利用することもできます)。

..  figure:: attachment/asakusa-runtime.png
    :width: 640px

Asakusa DSL
  従来のAsakusa DSLやDMDLで記述したバッチアプリケーションは基本的に変更なしで、\ |M3BP_COMPILER|\ を利用して\ |M3BP_ENGINE|\ 上で実行可能なジュールを生成することができます。

テスト機構
  従来のAsakusa DSLのテスト方法と同様に、テストドライバーを利用してAsakusa DSLのテストを実行することができます。このとき、\ |M3BP_FEATURE|\ は特に利用しません。

アプリケーションの実行
  従来と同様、YAESSを利用してバッチアプリケーションを実行することができます。
  実行環境にMapReduce用、Spark用、\ |M3BP_ENGINE|\ 用のバッチアプリケーションをすべて配置して運用することも可能です。

外部システム連携
  Direct I/OやWindGateといった外部システム連携モジュールは\ |M3BP_FEATURE|\ のバッチアプリケーションでもそのまま利用することができます。

..  attention::
    |M3BP_FEATURE|\ を利用する上でもWindGateなどの外部システム連携機能において、一部Hadoopの機能を利用します。

..  _m3bp-target-platform:

対応プラットフォーム
====================

実行環境
--------

|M3BP_FEATURE|\ は、今のところ64ビットx86アーキテクチャのLinux環境 (以下、Linux x64)上のみで動作の確認を行っています。

|M3BP_FEATURE|\ のアプリケーションを実行する場合、以下または互換のソフトウェアが必要になります。

* Java SE Development Kit 8 Update 74 (Linux x64)
* GNU C++ Library 4.8.5 (``libstdc++.so.6``)
* GNU C Library 2.17 (``libc.so.6``)
* Portable Hardware Locality 1.7 (``libhwloc.so.5``) [#]_

..  hint::
    上記の構成は、Red Hat Enterprise Linux 7.2 (またはCentOS 7.2などのクローン)を想定しています。
    これらのディストリビューションを利用している場合、標準のパッケージ管理ツールで上記の一部を導入できます。

..  [#] https://www.open-mpi.org/projects/hwloc/

Hadoopディストリビューション
----------------------------

|M3BP_FEATURE|\ は、実行環境にインストールされたHadoopと連係して動作することもできます。

以下のような機能を利用できます。

* Direct I/O

  * 入出力データソースに、HDFSやその他のHadoopが対応しているファイルシステムを利用

* WindGate

  * HDFSを経由してWindGateの入出力を授受

Hadoopとの連携方法は、 `Hadoopとの連携`_ を参照してください。

|M3BP_FEATURE|\ が動作を検証しているHadoopディストリビューションは、
:doc:`../product/target-platform` の「Hadoopディストリビューション」を参照してください。

..  attention::
    |M3BP_FEATURE| をMapRと連携して利用する場合において、バッチアプリケーションの起動時にデッドロックが発生しアプリケーションが実行されないことがある問題を確認しています。
    この問題の回避方法について `Hadoopとの連携`_ に記載しています。

開発環境の構築
==============

バッチアプリケーションの開発環境には、通常のAsakusa Frameworkの開発環境に加え、実行環境上で動作するネイティブライブラリをビルドするための環境が必要となります。

|M3BP_FEATURE|\ を利用して実行モジュールを作成するには、以下または互換のソフトウェアが必要になります。

* Java SE Development Kit 8 Update 74
* CMake 2.8 [#]_
* GNU Make 3.82 [#]_
* GNU Compiler Collection 4.8.5 (Linux x64) [#]_

  * gcc
  * g++

..  attention::
    ビルド環境と実行環境が異なる場合、実行環境で動作するオブジェクトコードを生成するためのクロスコンパイラが必要になります。
    オブジェクトコードの生成時にはCMakeを内部的に利用しているため、クロスコンパイラの設定もCMakeの機能を利用して行うことができます。

    クロスコンパイラを導入したら、\ |M3BP_COMPILER|\ のコンパイラオプション
    ``m3bp.native.cmake.CMAKE_TOOLCHAIN_FILE`` にCMakeのツールチェインファイルを指定してください。

    参考URL: https://cmake.org/Wiki/CMake_Cross_Compiling

..  hint::
    通常のAsakusa Frameworkの開発環境を準備するには以下のドキュメントなどを参考にしてください。

    * :doc:`../introduction/start-guide`
    * :basic-tutorial:`Asakusa Framework チュートリアル <index.html>`

..  [#] https://cmake.org/
..  [#] https://www.gnu.org/software/make/
..  [#] https://gcc.gnu.org/


アプリケーションの開発
======================

開発環境上で Asakusa Frameworkのバッチアプリケーションを開発し、\ |M3BP_FEATURE|\ のアプリケーションをビルドする方法を見ていきます。

プロジェクトテンプレート
------------------------

|M3BP_FEATURE|\ を利用する構成を持つアプリケーション開発用のプロジェクトテンプレートは、以下リンクからダウンロードします。

* `asakusa-m3bp-template-0.10.2.tar.gz <http://www.asakusafw.com/download/gradle-plugin/asakusa-m3bp-template-0.10.2.tar.gz>`_

..  seealso::
    プロジェクトテンプレートの構成や利用方法については、 :doc:`../application/gradle-plugin` を参照してください。

サンプルアプリケーション
------------------------

`サンプルプログラム集 (GitHub)`_ に含まれるプロジェクト ``example-basic-m3bp`` は |M3BP_FEATURE|\ を利用する基本的なサンプルアプリケーションプロジェクトです。

このプロジェクトは |M3BP_FEATURE|\ 用のプロジェクトテンプレートに対して、 :doc:`../introduction/start-guide` などで説明しているサンプルアプリケーション「カテゴリー別売上金額集計バッチ」用のソースコードが追加されています。

..  _`サンプルプログラム集 (GitHub)`: http://github.com/asakusafw/asakusafw-examples

..  _user-guide-gradle-plugin:

|M3BP_FEATURE| Gradle Plugin
----------------------------

|M3BP_FEATURE| Gradle Pluginは、アプリケーションプロジェクトに対して\ |M3BP_FEATURE|\ のさまざまな機能を追加します。

`プロジェクトテンプレート`_ や `サンプルアプリケーション`_ で紹介したプロジェクトには、 \ |M3BP_FEATURE| Gradle Pluginがあらかじめ利用可能になっています。

その他のプロジェクトで  \ |M3BP_FEATURE|  Gradle Pluginを有効にするには、アプリケーションプロジェクトのビルドスクリプト ( :file:`build.gradle` )に対して以下の設定を追加します。

* ``apply plugin: 'asakusafw-m3bp'``

以下は\ |M3BP_FEATURE| Gradle Pluginの設定を追加したビルドスクリプトの例です。

..  literalinclude:: attachment/build.gradle
    :language: groovy
    :caption: build.gradle
    :name: build.gradle-m3bp-user-guide-1

..  seealso::
    |M3BP_FEATURE| Gradle Pluginのより詳細な情報は、 :doc:`../application/gradle-plugin-reference` や :doc:`reference` などを参照してください。

アプリケーションのビルド
------------------------
:ref:`user-guide-gradle-plugin` を設定した状態で、Gradleタスク :program:`m3bpCompileBatchapps` を実行すると、\ |M3BP_FEATURE|\ 向けのバッチアプリケーションのビルドを実行します。

..  code-block:: sh

    ./gradlew m3bpCompileBatchapps

:program:`m3bpCompileBatchapps` タスクを実行すると、アプリケーションプロジェクトの :file:`build/m3bp-batchapps` 配下にビルド済みのバッチアプリケーションが生成されます。

標準の設定では、\ |M3BP_FEATURE|\ のバッチアプリケーションは接頭辞に ``m3bp.`` が付与されます。
例えば、サンプルアプリケーションのバッチID ``example.summarizeSales`` の場合、\ |M3BP_FEATURE|\ のバッチアプリケーションのバッチIDは ``m3bp.example.summarizeSales`` となります。

..  seealso::
    |M3BP_COMPILER|\ で利用可能な設定の詳細は、 :doc:`reference` を参照してください。

デプロイメントアーカイブの生成
------------------------------

:ref:`user-guide-gradle-plugin` を設定した状態で、Asakusa Frameworkのデプロイメントアーカイブを作成すると、\ |M3BP_FEATURE|\ のバッチアプリケーションアーカイブを含むデプロイメントアーカイブを生成します。

デプロイメントアーカイブを生成するには Gradleの :program:`assemble` タスクを実行します。

..  code-block:: sh

    ./gradlew assemble

..  hint::
    Shafuを利用する場合は、プロジェクトを選択してコンテキストメニューから :menuselection:`Jinrikisha (人力車) --> Asakusaデプロイメントアーカイブを生成` を選択します。

..  _m3bp-user-guide-using-hadoop:

Hadoopとの連携
--------------

..  attention::
    Hadoopとの連携についての標準の動作および設定は、Asakusa Framework バージョン 0.10.0 から大きく変更されました。
    バージョン0.9系、およびそれ以前のバージョンから移行する場合、必ず :doc:`../application/gradle-plugin-v010-changes` を参照してください。

`デプロイメントアーカイブの生成`_\ を行う際に、標準の設定では実行環境上にインストールしたHadoopと連携するようデプロイメントアーカイブを生成します。
実行環境上にインストールしたHadoopと連携することで、環境上に構築されているHDFSなどに対してファイルの入出力を行うことができるようになります。

実行環境にインストールされたHadoopを利用する際、以下の順序で ``hadoop`` コマンドを探して利用します (上にあるものほど優先度が高いです)。

* 環境変数に ``HADOOP_CMD`` が設定されている場合、 ``$HADOOP_CMD`` コマンドを経由して起動します。
* 環境変数に ``HADOOP_HOME`` が設定されている場合、 :file:`$HADOOP_HOME/bin/hadoop` コマンドを経由して起動します。
* :program:`hadoop` コマンドのパスが通っている場合、 :program:`hadoop` コマンドを経由して起動します。

..  warning::
    多くのHadoopコマンドは、Java VMのヒープ容量の最大値に非常に小さな値を標準で指定します。
    この設定を上書きする方法は、 `Java VMの設定`_ を参照してください。

..  attention::
    MapRなどの一部の環境では、バッチアプリケーション起動時にデッドロックが発生しアプリケーションが正しく実行されないことがある問題が確認されています。
    これを回避するには、 ``build.gradle`` に以下の設定を加えてください

    ..  code-block:: groovy
        :caption: build.gradle
        :name: build.gradle-m3bp-user-guide-3

        asakusafwOrganizer {
            extension {
                libraries += ["com.asakusafw.m3bp.bridge:asakusa-m3bp-workaround-hadoop:${asakusafw.m3bp.version}"]
            }
        }

また、実行環境のHadoopと連携せずローカルファイルシステムや外部のデータベースに対してのみデータの入出力を行うような場合でも、
Direct I/OやWindGateなどの一部のコンポーネントはHadoopに含まれるライブラリやスクリプトを必要とするため、
実行環境上にはAsakusa Frameworkの実行に必要なHadoopコンポーネントを導入する必要があります。

このような場合 Asakusa Gradle Plugin の機能で、必要な最低限のHadoopライブラリーをデプロイメントアーカイブに組み込むことができます。
デプロイメントアーカイブにHadoopライブラリーを含めるには、以下の設定を追加してください。

* ``asakusafwOrganizer.hadoop.embed true``

以下は、 ``prod`` プロファイルのデプロイメントアーカイブに対してのみ上記の設定を行う例です。

..  literalinclude:: attachment/build-hadoop-embed.gradle
    :language: groovy
    :caption: build.gradle
    :name: build.gradle-m3bp-user-guide-2
    :emphasize-lines: 19

..  attention::
    この方法で導入されるHadoopはAsakusa Frameworkの実行に最低限必要なコンポーネントのみが含まれます。
    特にHDFSなどのHadoopファイルシステム実装ライブラリが含まれないなどの制約があるため、
    実行環境上のHadoopファイルシステムと連携する場合にはこのオプションを有効にせず、実行環境上にインストールしたHadoopと連携するようにしてください。

..  tip::
    バッチアプリケーション実行時の環境変数は、YAESSプロファイルで設定することも可能です。

    \ |M3BP_FEATURE|\ を利用する場合、コマンドラインジョブのプロファイル ``command.m3bp`` が利用できます。 :file:`$ASAKUSA_HOME/yaess/conf/yaess.properties` に ``command.m3bp.env.HADOOP_CMD`` といったような設定を追加することで、YAESSから\ |M3BP_FEATURE|\ を実行する際に環境変数が設定されます。

    YAESSのコマンドラインジョブの設定方法について詳しくは、 :doc:`../yaess/user-guide` - :ref:`yaess-profile-command-section` などを参照してください。

アプリケーションの実行
======================

ここでは、\ |M3BP_FEATURE|\ 固有の実行環境の設定について説明します。

Asakusa Frameworkの実行環境の構築方法やバッチアプリケーションを実行する方法の基本的な流れは、 :doc:`../administration/deployment-guide` などを参照してください。

バッチアプリケーションの実行
----------------------------

デプロイしたバッチアプリケーションをYAESSを使って実行します。

:program:`$ASAKUSA_HOME/yaess/bin/yaess-batch.sh` コマンドに実行するバッチIDとバッチ引数を指定してバッチを実行します。
標準の設定では、\ |M3BP_FEATURE|\ のバッチアプリケーションはバッチIDの接頭辞に ``m3bp.`` が付与されているので、このバッチIDを指定します。

..  attention::
    標準の設定では、バッチIDの接頭辞に ``m3bp.`` がついていないバッチIDは従来のHadoop MapReduce向けバッチアプリケーションです。YAESSの実行時にバッチIDの指定を間違えないよう注意してください。

例えば、サンプルアプリケーションを実行する場合は、以下のように :program:`yaess-batch.sh` を実行します。

..  code-block:: sh

    $ASAKUSA_HOME/yaess/bin/yaess-batch.sh m3bp.example.summarizeSales -A date=2011-04-01

..  seealso::
    サンプルアプリケーションのデプロイやデータの配置、実行結果の確認方法などは、 :doc:`../introduction/start-guide` - :ref:`startguide-running-example` を参照してください。

..  attention::
    |M3BP_FEATURE|\ ではメモリ上に中間データを配置するため、入力データが膨大であったり中間データが膨らむようなバッチ処理では、メモリ容量が不足してしまう場合があります。この場合、バッチ処理はエラーにより中断されます。

    空きメモリ容量を増やすか、またはAsakusa on Sparkなどの利用を検討してください。

    この制約は将来緩和される可能性があります。

Java VMの設定
-------------

|M3BP_FEATURE|\ でバッチアプリケーションを実行する際には、Java VMをひとつ起動してそのプロセス内で\ |M3BP_ENGINE|\ やAsakusaの演算子を実行します。

このとき、対象のJava VMを起動する際のオプション引数を、環境変数 ``ASAKUSA_M3BP_OPTS`` で指定できます。

以下は環境変数の設定例です。

..  code-block:: sh

    export ASAKUSA_M3BP_OPTS='-Xmx16g'

上記のように書いた場合、Javaのヒープ領域の最大値を ``16GB`` に設定できます。

実行コマンドの設定
------------------

|M3BP_FEATURE|\ 実行用のJVMプロセスを起動するJavaコマンドは、環境変数 ``JAVA_CMD`` で設定することができます。
``JAVA_CMD`` が未設定の場合、 ``PATH`` 環境変数に含まれる ``java`` コマンドが使用されます。

`Hadoopとの連携`_ を設定した場合、\ |M3BP_FEATURE|\実行用のJVMプロセスを起動するコマンドには ``hadoop`` コマンドが使用されます。
この場合に利用される ``hadoop`` コマンドの検索方法は `Hadoopとの連携`_ の説明を参照してください。

環境変数 ``ASAKUSA_M3BP_LAUNCHER`` は実行コマンドの先頭に任意のコマンド文字列を追加します。

ログの設定
----------

|M3BP_FEATURE|\ の実行時のログ設定は、Logback設定ファイル ``$ASAKUSA_HOME/m3bp/conf/logback.xml`` で設定します。

..  attention::
    `Hadoopとの連携`_ を設定してバッチアプリケーションを実行した際に、利用する環境によってはバッチアプリケーションのログがHadoopのログ設定の上で出力される可能性があります。

    \ |M3BP_FEATURE|\ のログ設定を優先したい場合は、環境変数 ``HADOOP_USER_CLASSPATH_FIRST=true`` を設定してください。
