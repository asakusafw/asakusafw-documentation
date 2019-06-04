===============================================
Asakusa Gradle Plugin バージョン 0.9系 の変更点
===============================================

ここでは、Asakusa Gradle Plugin バージョン 0.8系 から 0.9系 の変更点について説明します。

Asakusa Gradle Pluginを利用したアプリケーションプロジェクトのマイグレーションについては、 :doc:`gradle-plugin-migration-guide` も参照してください。

ディストリビューションプラグイン
================================

Asakusa Gradle Pluginを利用する場合、これまではアプリケーションプロジェクトのビルドスクリプト ``build.gradle`` の ``buildscript`` ブロック内に利用するプラグインの定義を記述していました。

例えば Asakusa on Spark と |M3BP_FEATURE| を利用する場合、
以下のように各コンポーネントが提供するそれぞれのGradle Pluginを記述していました。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-gradle-plugin-v09-changes-1
    :emphasize-lines: 6-7

    buildscript {
        repositories {
            maven { url 'http://asakusafw.s3.amazonaws.com/maven/releases' }
        }
        dependencies {
            classpath group: 'com.asakusafw.spark', name: 'asakusa-spark-gradle', version: '0.3.1'
            classpath group: 'com.asakusafw.m3bp', name: 'asakusa-m3bp-gradle', version: '0.1.2'
        }
    }

0.9系以降では、それぞれのGradle Pluginを記述する代わりにディストリビューションプラグイン ``com.asakusafw.gradle:asakusa-distribution`` の利用を推奨します。

以下は、ビルドスクリプトにディストリビューションプラグインを適用する例です。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-gradle-plugin-v09-changes-2
    :emphasize-lines: 6

    buildscript {
        repositories {
            maven { url 'http://asakusafw.s3.amazonaws.com/maven/releases' }
        }
        dependencies {
            classpath group: 'com.asakusafw.gradle', name: 'asakusa-distribution', version: '0.9.0'
        }
    }

ディストリビューションプラグインはAsakusa Frameworkのリリース時に動作検証を行った各サブプロジェクトの組み合わせによる
Gradle Pluginのバージョンを自動的に適用し、これらを単一のバージョンで利用できるようにします。
将来サブプロジェクトが追加された場合や構成が変更になった場合にも、マイグレーションの手順がシンプルになります。

例えば、ディストリビューションプラグインのバージョン 0.9.0 は以下のGradle Pluginを自動的に適用します。

* ``com.asakusafw:asakusa-gradle-plugins:0.9.0``
* ``com.asakusafw.spark:asakusa-spark-gradle:0.4.0``
* ``com.asakusafw.m3bp:asakusa-m3bp-gradle:0.2.0``

..  attention::
    ディストリビューションプラグインを利用しない従来の方法でプラグインの定義を記述した場合、
    プラグインの定義に互換がないバージョンの組み合わせを設定できてしまうという問題があります。
    問題の一例として、それぞれのプラグインが利用するコアライブラリのバージョンが異なるため、
    実行時に互換がない実行ライブラリを使用してしまう、といった可能性があります。

アプリケーションSDKライブラリ
=============================

アプリケーションプロジェクトでバッチアプリケーションの開発に必要なライブラリを利用するために、
これまではAsakusa Frameworkのライブラリをグループ化したSDKアーティファクト（ :doc:`sdk-artifact` ）を提供していました。

例えばアプリケーションのプロジェクトテンプレートの標準設定では、
ビルドスクリプトの ``dependencies`` ブロック内にSDKアーティファクトの定義を記述していました。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-gradle-plugin-v09-changes-3

    dependencies {
        compile group: 'com.asakusafw.sdk', name: 'asakusa-sdk-core', version: asakusafw.asakusafwVersion
        compile group: 'com.asakusafw.sdk', name: 'asakusa-sdk-directio', version: asakusafw.asakusafwVersion
        compile group: 'com.asakusafw.sdk', name: 'asakusa-sdk-windgate', version: asakusafw.asakusafwVersion
        testRuntime group: 'com.asakusafw.sdk', name: 'asakusa-sdk-test-emulation', version: asakusafw.asakusafwVersion
    }

0.9系以降では、上の例にある標準的なアプリケーションSDKライブラリはプロジェクトの依存ライブラリに自動的に追加されるようになりました。

このため、特別な理由がない限り、上記の例に示すSDKアーティファクトの定義はビルドスクリプトから削除することを推奨します。

アプリケーションSDKライブラリに関する設定を変更する場合、ビルドスクリプトの ``asakusafw`` ブロック配下の ``sdk`` で指定します。

試験的機能として提供している Direct I/O Hive 用のSDKアーティファクト ``com.asakusafw.sdk:asakusa-sdk-hive`` を利用している場合、
標準の構成にはこのライブラリは含まれていないため、 ``dependencies`` ブロックから従来の定義を削除した上で、以下の定義を追加してください。

..  code-block:: groovy
    :caption: build.gradle
    :name: build.gradle-gradle-plugin-v09-changes-4

    asakusafw {
        sdk.hive true
    }

その他、アプリケーションプロジェクトで利用するSDKアーティファクトの定義を変更している場合は、
:doc:`gradle-plugin-reference` - :ref:`batch-application-plugin-reference` の「SDKプロパティ」の内容を確認して必要な設定を行ってください。

..  attention::
    ``dependencies`` ブロック内に :doc:`sdk-artifact` に記載しているSDKアーティファクト以外の定義を追加している場合は、その定義はそのまま残しておく必要があります。

    ``dependencies`` に定義を追加している主なケースには、演算子内で使用する任意のJavaライブラリを追加している場合や、 :doc:`../sandbox/index` として提供しているコンパイラ拡張ライブラリを使用している場合などがあります。

Asakusa Frameworkバージョンの指定
=================================

バージョン 0.8.1 より、 ビルドスクリプト上の ``asakusafw.asakusafwVersion`` を利用したAsakusa Frameworkバージョンの指定は非推奨機能となりましたが、バージョン0.9系以降では、 この値をビルドスクリプト上で変更してもこの設定は無効になるよう変更されました。

また、これまではビルドスクリプトの ``asakusafwOrganizer`` ブロック ``dependencies`` ブロック内でAsakusa Frameworkのライブラリを指定する場合にも ``asakusafw.asakusafwVersion`` を利用していましたが、0.9系以降ではこれに代わり以下のプロパティを利用することを推奨します。

..  list-table:: バージョンを保持するプロパティ
    :widths: 2 3
    :header-rows: 1

    * - プロパティ名
      - 説明
    * - ``asakusafw.core.version``
      - コアライブラリのバージョン。
    * - ``asakusafw.mapreduce.version``
      - Asakusa on MapReduceのバージョン。
    * - ``asakusafw.spark.version``
      - Asakusa on Sparkのバージョン。
    * - ``asakusafw.m3bp.version``
      - |M3BP_FEATURE| のバージョン。

プロパティの利用例は、 :doc:`../sandbox/directio-tsv` の設定例などを参照してください。

デプロイメントアーカイブファイル名の変更
========================================

これまでは、アプリケーションプロジェクトで :program:`assemble` タスクなどを実行して生成するデプロイメントアーカイブのファイル名は、標準で以下のファイル名を持っていました。

* 標準プロファイル: ``asakusafw-${asakusafwVersion}.tar.gz``
* 追加プロファイル: ``asakusafw-${asakusafwVersion}-<profile-name>.tar.gz``

0.9系以降では、標準で以下のファイル名に変更になりました。

* 標準プロファイル: ``asakusafw-${project.name}.tar.gz``
* 追加プロファイル: ``asakusafw-${project.name}-<profile-name>.tar.gz``
