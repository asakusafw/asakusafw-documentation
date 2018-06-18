==================================================
エミュレーションモードによるアプリケーションテスト
==================================================

この文書では、エミュレーションモードを利用したアプリケーションのテストについて説明します。

エミュレーションモード
======================

エミュレーションモードを有効にしてAsakusa DSLのテストを実行すると、Asakusa Frameworkが提供するラッパー機構を利用してHadoopの処理を実行します。

エミュレーションモードではテストを実行しているプロセス内でほとんどの処理を行うため、デバッグモードのブレークポイントなどを利用できるようになります。

..  attention::
    本機能はアプリケーションプロジェクトのHadoopライブラリを利用するため、標準で設定されたものと異なるHadoopディストリビューションやバージョンを利用する際に、正しく動かない可能性があります。

..  hint::
    エミュレーションモードを有効にしていない場合、テスト実行時にコマンドラインインターフェースを利用して、別プロセスで様々な処理を行います。

    別プロセスで動作させたほうが Java VM 上の問題は起こりにくくなるため、エミュレーションモード利用時に正しく動かない場合には、本機能を無効化して動作を確認してみることを推奨します。

..  hint::
    エミュレーションモードを使用することで、Windows環境でテストドライバーを使ったテストの実行が可能となります。

    Windows環境でエミュレーションモードを使った開発環境の設定例については、 :doc:`../introduction/start-guide-windows` を参照してください。

フローDSL/バッチDSLのテスト
---------------------------

エミュレーションモードを有効にして :ref:`データフローのテスト <testing-userguide-dataflow-testing>` を行うと、IDEからブレークポイントを指定してデータフロー内の演算子メソッドの動作を確認したり、カバレッジツールと連携して演算子メソッドのテストカバレッジを確認しやすくなります。

インテグレーションテスト
------------------------

:ref:`バッチテストランナー <testing-userguide-integration-test>` とエミュレーションモードを併用すると、インテグレーションテスト時のデバッグ作業がやりやすくなります。

エミュレーションモードの利用方法
================================

Asakusa Framework バージョン 0.8.0 以降では、:doc:`../introduction/start-guide` や :doc:`../application/gradle-plugin` などで説明しているプロジェクトテンプレートを利用する場合、
標準でエミュレーションモードが利用されます。

エミュレーションモードの設定
----------------------------

アプリケーションプロジェクトでエミュレーションモードの設定を変更する場合は、ビルドスクリプトの ``asakusafw`` ブロック内の ``sdk.testkit`` の値を変更します。

以下は、エミュレーションモードを利用を明示的に設定する例です。この設定は :doc:`../application/gradle-plugin` を利用する標準の構成と同じ設定です。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-emulation-mode-1

    asakusafw {
        sdk.testkit 'mapreduce-emulation'
    }

エミュレーションモードの設定を無効化し、環境のHadoopを利用するには以下のように設定します。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-emulation-mode-2

    asakusafw {
        sdk.testkit 'mapreduce'
    }

..  attention::
    通常はエミュレーションモードの利用を推奨しています。
    エミュレーションモードが正常に動作しないなどの場合にのみ、この設定変更を検討してください。

..  tip::
    エミュレーションモードを有効する別の方法として、ビルドスクリプトにはモジュール設定を記述せず、 :jinrikisha:`Shafu<shafu.html>` の機能を使ってEclipse上で設定する方法があります。
    この方法で設定を行うと、Eclipse上でのみエミュレーションモードが有効になります。
    詳しくは :jinrikisha:`Shafu<shafu.html>` の「設定」の説明を参照してください。

Gradle上でのテストドライバー実行
--------------------------------

`エミュレーションモードの設定`_ を有効化した状態でGradleの :program:`test` タスクを実行すると、テストドライバーがエミュレーションモードで実行されます。

..  tip::
    エミュレーションモードを有効にして Gradle上でテストを実行すると、Gradleが提供する `JaCoCo Plugin <http://www.gradle.org/docs/current/userguide/jacoco_plugin.html>`_ などのソースコードカバレッジ取得機能との連携が可能になります。

..  attention::
    Asakusa Framework バージョン |version| において、Windows上でエミュレーションモードを有効してテストドライバーを実行した際に以下のようなエラーログが出力されることがありますが、動作上は問題ありません。

    ..  code-block:: none

        INFO  インプロセステスト実行用の機能をテストドライバーにインストールしています
        INFO  インプロセステスト実行用の最適化設定をテストドライバーにインストールしています
        ERROR Failed to locate the winutils binary in the hadoop binary path
        java.io.IOException: Could not locate executable null\bin\winutils.exe in the Hadoop binaries.
            at org.apache.hadoop.util.Shell.getQualifiedBinPath(Shell.java:356) [hadoop-common-2.7.2.jar:na]
            ...

Eclipse上でのテストドライバー実行
---------------------------------

`エミュレーションモードの設定`_ を有効化した状態でGradleの :program:`eclipse` タスクを実行すると、Eclipse上でアプリケーションプロジェクトに対してエミュレーションモードが有効になります。

この状態でEclipseからテストドライバーを利用するテストクラスやバッチテストランナーを実行すると、テストドライバーがエミュレーションモードで実行されます。

..  tip::
    エミュレーションモードを有効にすると、テストドライバーを使ったテストクラスのデバッグ実行時にEclipseのブレークポイント機能などを利用できます。

実行モードの選択
----------------

..  attention::
    通常の場合、ここで説明する設定は不要です。
    旧バージョンからのマイグレーション後にエミュレーションモードが正常に動作しない場合にのみ、ここで説明する設定を有効にして動作を確認してください。

標準の設定では、 ``com.asakusafw.sdk:asakusa-sdk-test-emulation`` を指定したエミュレーションモードの実行時にはスモールジョブ実行エンジンが使用されます。

エミュレーションモードをスモールジョブ実行エンジンを使用しない設定で実行するには、テストドライバー実行時に以下のシステムプロパティを設定します。

``asakusa.testdriver.configurator.inprocess.optimize``
  * ``true``: エミュレーションモードでスモールジョブ実行エンジンを使用する(デフォルト)
  * ``false``: エミュレーションモードでスモールジョブ実行エンジンを使用しない

..  attention::
    Asakusa Framework バージョン ``0.7.2`` 以前では ``com.asakusafw:asakusa-test-inprocess`` を指定したエミュレーションモードの実行にはスモールジョブ実行エンジンは使用されませんでしたが、バージョン ``0.7.3`` からはスモールジョブ実行エンジンを使用するよう変更されました。

..  seealso::
    スモールジョブ実行エンジンについては、 :doc:`../mapreduce/configure-task-optimization` を参照してください。

