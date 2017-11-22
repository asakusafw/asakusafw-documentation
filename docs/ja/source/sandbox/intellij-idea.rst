===================
IntelliJ IDEAの利用
===================

この文書では、 `IntelliJ IDEA`_ 上でAsakusa Frameworkのバッチアプリケーションを開発するための設定手順などを説明します。

..  attention::
    Asakusa Framework バージョン |version| では、 IntelliJ IDEAの利用は試験的機能として提供しています。
    将来のバージョンで本書の設定手順などが変更になる可能性があります。

    本書では、 IntelliJ IDEA バージョン 2017.x を使った利用方法を説明します。
    バージョンによっては本書とは異なる画面やメニュー体系になっている場合がありますので、
    詳しくは IntelliJ IDEA のヘルプドキュメントなどを確認してください。

..  _`IntelliJ IDEA`: https://www.jetbrains.com/idea/

Gradle Wrapperの設定
====================

IntelliJ IDEA上で :doc:`../application/gradle-plugin` に記載のプロジェクトテンプレート ( :ref:`download-gradle-project-template` ) や
これをベースにした既存のアプリケーションプロジェクトをIntelliJ IDEAのGradleプロジェクトとしてインポートする場合、
そのままの設定ではプロジェクトに含まれるGradle WrapperをIntelliJ IDEAが認識しません。

IntelliJ IDEAにプロジェクトに含まれるGradle Wrapperを認識させるには、以下のように ``build.gradle`` に ``Wrapper`` タスクの設定を追加します。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-intellij-idea-1

    task wrapper(type: Wrapper) {
        gradleVersion = upgradeGradleWrapper.gradleVersion
        jarFile = upgradeGradleWrapper.jarFile
    }

IntelliJ IDEAの起動
===================

IntelliJ IDEAの起動時には、必ず環境変数 ``ASAKUSA_HOME`` が適用された状態で起動してください。

Project SDK (JDK) の登録
========================

IntelliJ IDEAの ``Project SDK`` にJDK8が登録されていない場合(IntelliJ IDEAをはじめて利用するなどの場合)、まずProject SDKにJDK8を登録します。

以下はProject SDKの設定手順例です。

1. IntelliJ IDEA起動時に表示される :guilabel:`Welcome Screen` の画面下部から :menuselection:`Configure --> Project Defaults --> Project Structure` を選択します。
2. :guilabel:`Default Project Structure` 画面で :menuselection:`New... --> JDK` を選択します。
3. :guilabel:`Select Home Directory for SDK` 画面で JDK8のインストールディレクトリを選択します。
4. :guilabel:`Default Project Structure` 画面に戻ったら :guilabel:`OK` ボタンを押下します。

  ..  figure:: attachment/idea-settings-project-sdk.png

プロジェクトのインポート
========================

IntelliJ IDEAを起動したら、プロジェクトテンプレートや既存のアプリケーションプロジェクトをIntelliJ IDEAにインポートします。
以下、インポートの手順例です。

1. IntelliJ IDEA起動時に表示される :guilabel:`Welcome Screen` から :guilabel:`Import Project` を選択します。
2. 表示されるダイアログでインポートするプロジェクトのディレクトリを選択します。
3. :guilabel:`Import Project` ダイアログで :guilabel:`Import project from external model` - :guilabel:`Gradle` を選択し、:guilabel:`Next` ボタンを押下します。
4. 続けて表示されるダイアログで以下のようにオプションを選択し、 :guilabel:`Finish` ボタンを押下します（以下に記載しない設定項目は任意です）。

  * :guilabel:`Create separate module per source set` : オフ [#]_
  * :guilabel:`Use gradle wrapper task configuration` : 選択 [#]_ [#]_

  ..  figure:: attachment/idea-import-gradle-project.png

..  [#] このオプションは IntelliJ IDEA 2016.1 以降のバージョンに存在します。現時点ではこのオプションをオンにするとAsakusa Gradle Pluginを適用したプロジェクトを正しくビルドすることができません。
..  [#] このオプションを選択するには、 `Gradle Wrapperの設定`_ の手順に従って ``build.gradle`` にWrapperタスクの設定を追加しておく必要があります。
..  [#] Gradle Wrapperを使用せず、ローカルにインストールしたGradleを使用する場合は :guilabel:`Use local gradle distribution` を選択します。

コンパイラと注釈プロセッサの設定
================================

インポートしたプロジェクト上でOperator DSLコンパイラを使用するために、IntelliJ IDEAのコンパイラと注釈プロセッサの設定を行います。

1. プロジェクトの設定画面を表示します [#]_ 。
2. 設定画面左のメニューから :menuselection:`Build, Execution, Deployment --> Compiler` を選択してコンパイラの設定画面を表示します。
3. コンパイラの設定画面で、 :guilabel:`Build project automatically` を オンにして、画面下部の :guilabel:`Apply` ボタンを押下します。

  ..  figure:: attachment/idea-settings-compiler.png

4. 設定画面左のメニューから :menuselection:`Build, Execution, Deployment --> Compiler --> Annotation Processors` を選択して注釈プロセッサの設定画面を表示します。
5. 注釈プロセッサの設定画面で以下のようにオプションを選択および入力し、 画面下部の :guilabel:`OK` ボタンを押下します。

  * :guilabel:`Enable annotation processing` : オン
  * :guilabel:`Obtain processors from project classpath` : 選択
  * :guilabel:`Store generated sources relative to` : :guilabel:`Module content root` を選択
  * :guilabel:`Production sources directory` : ``build/generated-sources/annotations``
  * :guilabel:`Test sources directory` : ``build/generated-sources/generated_tests`` [#]_

  ..  figure:: attachment/idea-settings-annotation-processors.png

..  [#] 設定画面の表示方法については、次のドキュメントなどを参照してください。 https://www.jetbrains.com/help/idea/accessing-settings.html
..  [#] 現時点でのAsakusa Frameworkでは使用しません。

Gradleタスクの実行
==================

IntelliJ IDEA上でGradleタスクを実行するには、 :guilabel:`Gradle Tool Window` を使うと便利です。

1. :menuselection:`View --> Tool Windows --> Gradle` を選択して :guilabel:`Gradle Tool Window` を表示します。
2. :guilabel:`Gradle Tool Window` ではプロジェクトで実行可能なGradleタスクを選択して実行できます。

  * :menuselection:`Tasks --> asakusa framework build` にはAsakusa Gradle Pluginが追加したアプリケーション開発用のタスクが含まれます。
  * :menuselection:`Tasks --> asakusa framework organizer` にはAsakusa Gradle Pluginが追加したデプロイ構成用のタスクが含まれます。
  * :menuselection:`Tasks --> build` にはGradleが標準で提供するビルド用のタスクが含まれます。

  ..  figure:: attachment/idea-gradle-tool-window.png
