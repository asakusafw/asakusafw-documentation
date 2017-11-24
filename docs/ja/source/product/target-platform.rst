====================
対応プラットフォーム
====================

Hadoopディストリビューション
============================

Asakusa Framework は、以下のHadoopディストリビューションと組み合わせた運用環境で動作を検証しています。

..  list-table:: 動作検証プラットフォーム(Hadoopディストリビューション)
    :header-rows: 1
    :widths: 4 2 4

    * - Distribution
      - Version
      - OS
    * - Hortonworks Data Platform
      - 2.6.2
      - CentOS 7.4
    * - MapR
      - 5.2.2 [#]_
      - CentOS 7.3
    * - CDH
      - 5.13.0 [#]_
      - CentOS 7.2
    * - Amazon EMR
      - 5.9.0
      - Amazon Linux 2017.09 based
    * - Microsoft Azure HDInsight
      - 3.6
      - Ubuntu 16.04.3

..  [#] MapReduce Version 1 (MRv1) には対応していません。
..  [#] MapReduce Version 1 (MRv1) には対応していません。

アプリケーション開発環境
========================

Asakusa Frameworkを利用したバッチアプリケーションの開発環境は、 以下のプラットフォームで動作を検証しています。

..  list-table:: 動作検証プラットフォーム(開発環境)
    :widths: 2 4 4
    :header-rows: 1

    * - 種類
      - Product
      - Version
    * - OS
      - Ubuntu Desktop
      - 16.04.3
    * - OS
      - Windows
      - 10 (1709)
    * - OS
      - MacOSX [#]_
      - 10.13
    * - Java
      - JDK [#]_ [#]_
      - 1.8.0_151
    * - ビルドツール
      - Gradle [#]_
      - 4.3.1
    * - IDE
      - Eclipse IDE for Java Developers
      - 4.7.1a
    * - IDE
      - IntelliJ IDEA Community Edition [#]_
      - 2017.2.6

..  [#] MacOSX上では基本的な動作のみ検証しています。
..  [#] JREでは一部の機能が動作しません。必ずJDKを使用してください。
..  [#] 開発環境に対するJavaのセットアップについては、 :doc:`../application/using-jdk` を参照してください。
..  [#] Gradleの利用については、 :doc:`../application/gradle-plugin` を参照してください。
..  [#] IntelliJ IDEAの利用は試験的機能として提供しています。詳しくは :doc:`../sandbox/intellij-idea` を参照してください。

WindGate
========

:doc:`WindGate <../windgate/index>` は以下のプラットフォームで動作を検証しています。

..  list-table:: 動作検証プラットフォーム(WindGate/JDBC [#]_ )
    :widths: 2 4 4
    :header-rows: 1

    * - 種類
      - Product
      - Version
    * - DBMS
      - PostgreSQL
      - 9.3
    * - JDBC Driver
      - PostgreSQL JDBC Driver
      - 9.1 Build 901

..  [#] データベースを利用しない場合(例えば WindGate/CSV のみを使う場合)には不要です

リンク
======

対応プラットフォームのリンク集です。

..  list-table::
    :widths: 2 8
    :header-rows: 1

    * - Product
      - Link
    * - Apache Hadoop
      - http://hadoop.apache.org/
    * - Hortonworks Data Platform
      - http://hortonworks.com/hdp/
    * - MapR
      - http://www.mapr.com/
    * - Cloudera CDH
      - http://www.cloudera.com/content/cloudera/en/products-and-services/cdh.html
    * - Amazon EMR
      - http://aws.amazon.com/elasticmapreduce/
    * - Microsoft Azure HDInsight
      - https://azure.microsoft.com/services/hdinsight/
    * - CentOS
      - http://www.centos.org/
    * - Ubuntu
      - http://www.ubuntu.com/
    * - Windows
      - http://windows.microsoft.com/
    * - MacOSX
      - http://www.apple.com/osx/
    * - JDK (Java SE)
      - http://www.oracle.com/technetwork/java/javase/index.html
    * - Gradle
      - http://www.gradle.org/
    * - Eclipse
      - http://www.eclipse.org/
    * - IntelliJ IDEA
      - https://www.jetbrains.com/idea/
    * - PostgreSQL
      - http://www.postgresql.org/
