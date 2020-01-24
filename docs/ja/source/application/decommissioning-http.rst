=======================================================
Maven Centralとgradle.orgのHTTP接続無効化の影響について
=======================================================

この文書では、2020/1/15にMaven Centralとgradle.orgに行われたHTTP接続の無効化（HTTPSによる接続のみ許可するよう変更）について、Asakusa Frameworkへの影響、および問題が発生した場合の対応方法を説明します。

Maven Centralとgradle.orgに行われたHTTP接続の無効化について詳しくは、それぞれ以下のドキュメントを参照してください。

* https://blog.sonatype.com/central-repository-moving-to-https
* https://blog.gradle.org/decommissioning-http

発生する問題
============

Maven Centralとgradle.orgがHTTP接続を受け付けなくなったことにより、Asakusa Frameworkの一部のバージョンでビルドエラーが発生することがあります。

なお、アプリケーションのビルドとは通常アプリケーションプロジェクト上で ``build`` タスクや ``assemble`` タスク等を実行して実行モジュールを生成することを言いますが、本書では ``installAsakusafw`` タスクの実行によるAsakusa Frameworkのインストール操作など、アプリケーションプロジェクトに対するGradleのタスク実行全般をまとめてビルドと表現しています。

Maven CentralへのHTTPアクセスによるビルドエラー
-----------------------------------------------

* 影響するAsakusa Frameworkのバージョン: ``0.6.0`` ～ ``0.10.3``

アプリケーションプロジェクト上でビルドを実行した際に、以下のようなエラーが出力されビルドが失敗します。

* ``Could not GET 'http://repo1.maven.org/maven2/com/asakusafw/<module>/<version>/<module>-<version>.pom'. Received status code 501 from server: HTTPS Required``

以下はエラーが発生する場合の ``gradlew`` コマンドの出力例です。

..  code-block:: sh

    ./gradlew installAsakusafw

    ...

    > Task :gatherAsakusafw_dev FAILED
    FAILURE: Build failed with an exception.
    * What went wrong:
    Could not resolve all files for configuration ':asakusafwCoreDist_dev'.
    > Could not resolve com.asakusafw:asakusa-runtime-configuration:0.10.3.
    Required by: 
        project :
    > Could not resolve com.asakusafw:asakusa-runtime-configuration:0.10.3.
        > Could not get resource 'http://repo1.maven.org/maven2/com/asakusafw/asakusa-runtime-configuration/0.10.3/asakusa-runtime-configuration-0.10.3.pom'.
            > Could not GET 'http://repo1.maven.org/maven2/com/asakusafw/asakusa-runtime-configuration/0.10.3/asakusa-runtime-configuration-0.10.3.pom'. Received status code 501 from server: HTTPS Required 

gradle.orgへのHTTPアクセスによるビルドエラー
--------------------------------------------

* 影響するAsakusa Frameworkのバージョン: ``0.6.0`` ～ ``0.9.0``

アプリケーションプロジェクト上でビルドを実行した際に、以下のようなエラーが出力されビルドが失敗します。

* ``Exception in thread "main" java.io.IOException: Server returned HTTP response code: 403 for URL: http://services.gradle.org/distributions/gradle-<version>-bin.zip``

以下はエラーが発生する場合の ``gradlew`` コマンドの出力例です。

..  code-block:: sh

    ./gradlew installAsakusafw
    ...
    Downloading http://services.gradle.org/distributions/gradle-3.1-bin.zip
    Exception in thread "main" java.io.IOException: Server returned HTTP response code: 403 for URL: http://services.gradle.org/distributions/gradle-3.1-bin.zip
            at sun.net.www.protocol.http.HttpURLConnection.getInputStream0(HttpURLConnection.java:1894)
            at sun.net.www.protocol.http.HttpURLConnection.getInputStream(HttpURLConnection.java:1492)
            at org.gradle.wrapper.Download.downloadInternal(Download.java:58)
            at org.gradle.wrapper.Download.download(Download.java:44)
            at org.gradle.wrapper.Install$1.call(Install.java:61)
            at org.gradle.wrapper.Install$1.call(Install.java:48)
            at org.gradle.wrapper.ExclusiveFileAccessManager.access(ExclusiveFileAccessManager.java:69)
            at org.gradle.wrapper.Install.createDist(Install.java:48)
            at org.gradle.wrapper.WrapperExecutor.execute(WrapperExecutor.java:107)
            at org.gradle.wrapper.GradleWrapperMain.main(GradleWrapperMain.java:61)

また :jinrikisha:`Shafu <shafu.html>` からビルドした場合は、エラーダイアログ ``不明なエラー`` に以下のような詳細メッセージが出力されビルドが失敗します。

* ``Cound not install Gradle distribution from 'http://services.gradle.org/distributions/gradle-<version>-bin.zip``

問題が発生する条件
------------------

開発環境やビルド環境で実際にこの問題が発生するかは、その環境の状態も影響します。

環境の状態で強く影響するのが、Gradleのリポジトリキャッシュ（ローカルキャッシュ）の状態です。
ビルド時に要求されるライブラリやモジュールがすべてローカルのリポジトリキャッシュで解決できる場合、Maven Centralやgradle.orgへのアクセスが発生せずにビルドが成功することがあります。

そのほか、リポジトリのキャッシュ更新の設定やオフラインオプションの設定、アプリケーションプロジェクトのリポジトリ設定なども、この問題の発生に影響することがあります。

対応方法
========

問題が発生した場合、以下で説明する対応方法を確認してください。

Asakusa Frameworkのバージョンアップ
-----------------------------------

Asakusa Framework バージョン ``0.10.4`` 以降にバージョンアップすることでこの問題は発生しなくなります。

バージョンアップ時の注意点として `gradle.orgへのHTTPアクセスによるビルドエラー`_ が発生した環境上でマイグレーションを行うには、通常のマイグレーション手順( :doc:`migration-guide` )を実施する前に、以下で説明する `gradle.orgへのHTTPアクセスによるビルドエラーが発生した場合の対応`_ の手順を実施する必要があります。

Asakusa Frameworkのバージョンアップを行わずに（現在のバージョンをそのまま利用しつつ）この問題に対応したい場合は、以下に説明する方法でビルドエラーを回避することができます。

Maven CentralへのHTTPアクセスによるビルドエラーが発生した場合の対応
-------------------------------------------------------------------

`Maven CentralへのHTTPアクセスによるビルドエラー`_ は、該当バージョンのAsakusa Gradle Pluginがアプリケーションプロジェクトに対してHTTPを含むMaven CentralのリポジトリURLをリポジトリ設定として登録するために発生します。

このため、ビルド設定でMaven CentralのURLをHTTPからHTTPSに変換することによって、ビルドエラーを回避することができます。
以下ではこの対応方法をいくつか説明します。

初期化スクリプトの利用
~~~~~~~~~~~~~~~~~~~~~~

Gradleの初期化スクリプトはビルドの初期化時にスクリプトを実行することでビルド設定をカスタマイズする仕組みです。
ビルド環境にMaven CentralのURLをHTTPからHTTPSに変換する初期化スクリプトを適用することで、
ビルドエラーを回避することができます。

以下は、Maven CentralのURLをHTTPからHTTPSに変換する初期化スクリプトの例です。

:download:`replace-repo-url-https.gradle <gradle-attachment/replace-repo-url-https.gradle>`

..  literalinclude:: gradle-attachment/replace-repo-url-https.gradle
    :language: groovy
    :caption: replace-repo-url-https.gradle
    :name: replace-repo-url-https.gradle

初期化スクリプトを環境に適用するにはいくつかの方法が提供されていますが、一例としてビルド実行ユーザのホームディレクトリ配下の ``.gradle/init.d`` ディレクトリに上記の ``replace-repo-url-https.gradle`` を配置します。
これにより、環境で実行されるすべてのビルドで自動的にこの初期化スクリプトが適用されます。

その他の初期化スクリプトの適用方法はGradleのドキュメント（ `Initialization Scripts`_ ）などを参照してください

なお、初期化スクリプトを使わずアプリケーションプロジェクトの ``build.gradle`` の変更のみで行いたい場合は、上記の初期化スクリプトと同等の処理を ``build.gradle`` に記述することによっても対応可能ですが、この方法は影響するすべてのアプリケーションプロジェクトに対して個別に行う必要があります。

..  _`Initialization Scripts`: https://docs.gradle.org/current/userguide/init_scripts.html

Shafuの利用
~~~~~~~~~~~

:jinrikisha:`Shafu <shafu.html>` バージョン 0.8.0 以降では、ビルド時に上記の初期化スクリプトで説明したMaven CentralのURLをHTTPからHTTPSに変換する処理が自動で適用されます。

利用しているShafuのバージョンを確認し、必要に応じてShafuのバージョンアップを実施してください。

gradle.orgへのHTTPアクセスによるビルドエラーが発生した場合の対応
----------------------------------------------------------------

`gradle.orgへのHTTPアクセスによるビルドエラー`_ は、該当バージョンのAsakusa Frameworkプロジェクトテンプレートに含まれるGradleラッパーの設定のうち、Gradleディストリビューションのダウンロード先がHTTPを含むURLになっているために発生します。

また、該当バージョンのAsakusa Gradle Pluginの ``asakusaUpgrade`` タスクを実行して導入されるGradleラッパーの設定についても、Gradleディストリビューションのダウンロード先がHTTPを含むURLになっています。

このため、GradleラッパーのGradleディストリビューションのダウンロードURLをHTTPからHTTPSに変更するか、Gradleラッパーを経由したダウンロード以外の方法で環境に導入したGradleディストリビューションを利用することで、ビルドエラーを回避することができます。以下ではこの対応方法をいくつか説明します。

Gradleラッパー設定ファイルの変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

この問題が発生するアプリケーションプロジェクトでは、Gradleラッパー設定ファイル ``.buildtools/gradlew.properties`` に設定されている ``distributionUrl`` が ``http`` からはじまるURLになっています。この部分を ``https`` に変更します。

以下は、この問題が発生する Asakusa Framework バージョン 0.9.0 に含まれる ``distributionUrl`` の ``http`` 部分を ``https`` に変更した ``gradlew.properties`` の例です。

..  literalinclude:: gradle-attachment/https-gradlew.properties
    :language: text
    :caption: gradlew.properties
    :name: https-gradlew.properties

上記設定後にビルドを行うことで、Gradleディストリビューションが正常にダウンロードされビルドエラー解消されます。

環境にインストールしたGradleディストリビューションを利用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gradleラッパーによって導入するGradleディストリビューションを使うのではなく、
事前に環境にインストールしたGradleディストリビューションを使う方法でもビルドエラーを回避することができます。

環境にGradleをインストールする方法は、Gradleのドキュメント（ `Installation`_ ） などを参照してください。

この方法では、Asakusa Frameworkの各バージョンで動作検証を行っているGradleバージョン以外のバージョンが利用される可能性があり、動作検証以外のバージョンを使うことによる問題が発生することがある点に注意してください。

..  _`Installation`: https://gradle.org/install/

Shafuの利用
~~~~~~~~~~~

:jinrikisha:`Shafu <shafu.html>` を使う場合、この問題が発生するかはShafuの以下の設定によります。

* 設定画面の ``[基本]`` タブ -> ``Gradleのバージョンをラッパーの設定情報から取得``

  * Shafu バージョン 0.7.0 以降はデフォルトで有効、これより前のバージョンは設定項目なし（無効と同じ設定で動作）

設定が有効である場合、ビルド対象のアプリケーションプロジェクトがこの問題の影響を受けるものである場合、ビルドエラーとなります。

設定が無効である場合はこの問題の影響を受けません。
ただし設定が無効の場合、上述の `環境にインストールしたGradleディストリビューションを利用`_ と同様に、動作検証を行っているGradleバージョン以外のバージョンが利用される可能性があります。

設定を無効にすることによるエラー回避は一時的なワークアラウンドとしては有効ですが、恒久的には `Gradleラッパー設定ファイルの変更`_ の対応方法を適用し、設定は有効にすることを推奨します。
