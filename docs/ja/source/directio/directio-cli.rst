=============================
Direct I/O CLI ユーザーガイド
=============================

この文書では、Direct I/O CLI ( :program:`directio` コマンド ) の利用方法について説明します。

..  experimental::
    Asakusa Framework バージョン |version| では、Direct I/O CLIは試験的機能として提供しています。

セットアップ
============

Direct I/O CLIは開発環境と運用環境の両方で利用することができます。

開発環境のセットアップ
----------------------

開発環境では、開発環境用のAsakusa Frameworkがインストールされた状態であればDirect I/O CLIを利用することができます。
開発環境上でAsakusa Frameworkをインストールする手順については、 :doc:`../introduction/start-guide` や :doc:`../application/gradle-plugin` などを参照してください。

運用環境のセットアップ
----------------------

運用環境では、Asakusa Frameworkのデプロイメントアーカイブを配備した状態であればDirect I/O CLIを利用することができます。
運用環境上でデプロイメントアーカイブを配置する手順については、 :doc:`../administration/deployment-guide` などを参照してください。

:program:`directio` コマンド
----------------------------

Direct I/O CLIの各機能は :program:`directio` コマンドを通して利用します。
セットアップが完了した環境であれば、 :program:`directio` コマンドは ``$ASAKUSA_HOME/tools/bin`` 配下に配置されています。
コマンドラインから :program:`directio` コマンドを利用する場合、 ``$ASAKUSA_HOME/tools/bin`` 配下に環境変数 ``PATH`` を通しておくと便利です。

以降本書で :program:`directio` コマンドを実行する例を示す際には、上記の ``PATH`` 環境変数が設定済であるものとします。

正しくセットアップが行われている環境でコマンドラインから :program:`directio` コマンドを実行すると、以下のように表示されます。

..  code-block:: sh

    $ directio
    使用方法: directio <command> <command options>

    利用可能なコマンドの一覧:
        configuration - Direct I/O の各種設定情報を表示する。
        copy - Direct I/O データソース上でリソースのコピーを行う。
        delete - Direct I/O のリソースを削除する。
        get - Direct I/O のリソースをローカルファイルシステム上にコピーする。
        list - Direct I/O のリソースを一覧表示する。
        mkdir - Direct I/O のデータソース上にディレクトリーを作成する。
        move - Direct I/O のデータソース上でリソースの移動を行う。
        put - ローカルファイルを Direct I/O のデータソースにコピーする。
        transaction - Direct I/O のトランザクションを操作する。

    各コマンドの詳しい情報は 'directio <command> --help' を参照してください。

上記が表示されず、エラーメッセージが表示されてしまう場合には、セットアップ環境を確認してください。

Hadoop環境の設定
----------------

Direct I/O CLIを利用するにはHadoop環境がセットアップされている必要があります。

まず、 :doc:`../m3bp/user-guide` - :ref:`m3bp-user-guide-using-hadoop` に示す手順などにより
``hadoop.embed true`` を指定してAsakusa Frameworkに組み込みのHadoopライブラリーを含めた場合、Direct I/O CLIはこれを使用します。

上記の設定を行わず、実行環境にインストール済みのHadoopと連携する場合、以下の環境変数のいずれかによって利用するHadoop環境を特定します。

``HADOOP_CMD``
  ``hadoop`` コマンドのパス
``HADOOP_HOME``
  Hadoopのインストール先
``PATH``
  :program:`hadoop` コマンドが通っているパス

上記の方法で利用可能なHadoopを解決できない場合、 :program:`directio` コマンドは実行時にエラーとなります。

Asakusa Frameworkが利用するHadoop環境(Hadoopライブラリーや :program:`hadoop` コマンドのパス)は、 :program:`asakusa` コマンド [#]_ で確認することができます。

..  code-block:: sh

    $ asakusa version -v
    0.10.0
    ASAKUSA_HOME: /home/asakusa/asakusa
    Hadoop: /usr/local/lib/hadoop/bin/hadoop
    java.version: 1.8.0_121
    java.vendor: Oracle Corporation

:program:`asakusa version -v` コマンドを実行した結果、 ``Hadoop:`` に表示されるHadoopライブラリーや :program:`hadoop` コマンドをDirect I/O CLIは利用します。
この値に ``N/A`` と表示される場合は利用可能なHadoopを解決できていない状態です。

..  [#] :program:`asakusa` コマンドについて詳しくは、 :doc:`../cli/index` を参照してください。

コマンド体系
============

サブコマンド
------------

:program:`directio` コマンドはサブコマンドを指定することで様々な機能を呼び出します。
サブコマンドには :program:`configuration` や :program:`list` 、 :program:`put` といったものがあります。
サブコマンドの中には、さらにサブコマンドを要求するものもあります。

コマンドラインから実行する際には、サブコマンド間をスペースで区切って指定します。

例えば、:program:`directio configuration list` のように実行すると、環境上に設定されたDirect I/Oのデータソースをリストとして表示します。

..  code-block:: sh

    $ directio configuration list
    root

パラメータ
----------

多くのサブコマンドでは、サブコマンドに続けて処理の対象を指定するパラメータを指定します。

コマンドラインから実行する際には、サブコマンドの後にパラメータをスペースで区切って指定します。

例えば、:program:`directio get` は1つ目のパラメータに指定したDirect I/O上のパス上のファイルを、2つ目のオプションで指定したローカルパス上に保存します。

..  code-block:: sh

    $ directio get result/category/result.csv /tmp

オプション
----------

各サブコマンドにはサブコマンド共通、または固有のオプションが存在します。

コマンドラインから実行する際には、サブコマンドの後、またはパラメータ後にスペースで区切って指定します。
多くのLinuxコマンドと同様に、いくつかのオプションでは ``--`` から始まる記法の他、 ``-`` から始まる短縮記法を利用できます。

オプションによっては、オプション固有のパラメータを指定するものもあります。
通常、オプションとそのパラメータはスペースで区切って指定しますが、
一部のオプションでは ``-Akey=value`` のようにスペースで区切らずに指定することも可能です。

以下はサブコマンドの主なオプションです。
サブコマンドによって使用できるオプションは異なるので、詳しくは各サブコマンドのヘルプを参照してください。

..  program:: directio subcommand common

..  option:: --conf, --configuration file

    Direct I/O CLIが利用するDirect I/O設定ファイルのファイルパスを指定する。

    既定値: ``$ASAKUSA_HOME/core/conf/asakusa-resources.xml``

..  option:: -s, --data-source

    データソースIDを指定し、対応するデータソースに対する操作を行う

..  option:: -e, --encoding encoding

    コマンドの出力内容の文字セットエンコーディングを指定する。

    デフォルトでは環境の標準エンコーディングを使用する。

..  option:: -o, --output file

    コマンドの出力内容を指定したファイルパスに保存する。
    デフォルトでは標準出力に出力する。

..  option:: -v, --verbose

    コマンド実行結果の出力に詳細な情報を含める。

..  option:: -h, --help

    ヘルプメッセージを表示する。
    サブコマンドが要求するオプションや追加のサブコマンドを確認する。

    ..  code-block:: sh

        $ directio list --help
        Usage: directio list [options] [directio-path..]
          Options:
            --conf, --configuration
              Hadoopの追加設定ファイルのパスを指定する。
              Default: /home/asakusa/asakusa/core/conf/asakusa-resources.xml
            -s, --data-source
              データソースIDを直接指定する（パスから推定したものを無視）。
            ...

コマンドリファレンス
====================

:program:`directio` コマンドのサブコマンド一覧を以下に示します。

..  list-table:: :program:`directio` サブコマンド
    :widths: 2 2 6
    :header-rows: 1

    * - サブコマンド
      - カテゴリ
      - 説明
    * - :ref:`directio-cmd-list`
      - ファイル操作
      - Direct I/Oのデータソースに含まれるファイルの一覧を表示する
    * - :ref:`directio-cmd-mkdir`
      - ファイル操作
      - Direct I/Oのデータソース上にディレクトリを作成する
    * - :ref:`directio-cmd-get`
      - ファイル操作
      - Direct I/Oのデータソース上のファイルをローカルファイルシステムにコピーする
    * - :ref:`directio-cmd-put`
      - ファイル操作
      - ローカルファイルシステム上のファイルをDirect I/Oのデータソース上にコピーする
    * - :ref:`directio-cmd-delete`
      - ファイル操作
      - Direct I/Oのデータソース上のファイルを削除する
    * - :ref:`directio-cmd-copy`
      - ファイル操作
      - Direct I/Oのデータソース間でファイルをコピーする
    * - :ref:`directio-cmd-move`
      - ファイル操作
      - Direct I/Oのデータソース間でファイルを移動する
    * - :ref:`directio-cmd-configuration`
      - 設定
      - Direct I/Oの設定を表示する
    * - :ref:`directio-cmd-transaction`
      - トランザクション
      - Direct I/Oのトランザクション操作を行う

ファイル操作について
--------------------

ここではファイル操作系のサブコマンドに共通するオプションや動作について説明します。

directio-path
~~~~~~~~~~~~~

コマンドのオプションに ``directio-path..`` (ファイル名のパターン)を指定する場合、ここにはファイル名だけでなくワイルドカードなどのパターン用の文字列も利用できます。

ここに利用できるパターンは以下の通りです。

..  list-table:: 利用できるパターン
    :widths: 10 10 40
    :header-rows: 1

    * - 文字列
      - 名前
      - 概要
    * - 名前文字
      - リテラル
      - そのままファイル名として利用します。
        対象のデータソースが利用できるファイル名のうち、
        ``/`` , ``\`` , ``$`` , ``*`` , ``?`` , ``#`` , ``|`` , ``{`` , ``}`` , ``[`` , ``]`` 以外の文字を利用できます。
    * - ``/``
      - 名前区切り
      - パスに含まれる名前の区切り文字です。
    * - ``*``
      - ワイルドカード
      - 0個以上の任意の名前文字とマッチします。
    * - ``{..|..|..}``
      - 選択
      - ``|`` で区切られたいずれかの名前にマッチします。
        ``..`` の部分には名前文字と名前区切りの組み合わせのみを指定できます。

上記のほかに、特別なディレクトリやファイル名として ``**`` を利用できます。
これは、検索対象以下のすべてのサブディレクトリ(自身のディレクトリも含む)とそれに含まれるファイルにマッチします。

ただし、 ``**`` はディレクトリやファイル名の一部としては利用できません。
たとえば、 ``**.csv`` というパターンは利用できず、代わりに ``**/*.csv`` と書きます。

..  attention::
    利用しているシェルによっては、 ``directio-path`` に ``*`` 文字が含まれていた場合に自動的に展開されてしまいます。
    展開を回避するには、 ``"*"`` のようにダブルクウォート文字で囲むなどの指定を行なってください。

:program:`directio` コマンドでは、上記の文法で指定したパスから、自動的にDirect I/Oのベースパスとリソースパターンを抽出します。

具体的には、パスの先頭から「名前区切り」ごとに「名前文字」のみで構成された部分をベースパスとして取り扱い、残りをリソースパターンとして取り扱います。
なお、パスの末尾の名前は常にリソースパターンとして扱い、ベースパスが空になった場合には ``/`` として扱います。

以下は例です。

* ``a/b/*.csv`` -> ``a/b`` + ``*.csv``
* ``a/b.csv`` -> ``a`` + ``b.csv``
* ``**/*.csv`` -> ``/`` + ``**/*.csv``

このパスは、以下のコマンドで利用します。

* :program:`directio list` の引数
* :program:`directio mkdir` の引数
* :program:`directio get` の先頭の引数 (コピー元)
* :program:`directio put` の末尾の引数 (コピー先)
* :program:`directio copy` の引数
* :program:`directio move` の引数

..  hint::
    Direct I/Oはベースパスの最長一致でデータソースを特定しています。
    上記とは異なる方法でデータソースを指定する場合、 ``--datasource`` オプションに対象のデータソースIDを指定してください。

ファイルの移動・コピーの動作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`directio` コマンドにおいて、下記のファイルの移動やコピーを行うコマンドは、移動・コピー先（宛先）に関する共通の動作があります。

* :program:`directio get`
* :program:`directio put`
* :program:`directio copy`
* :program:`directio move`

1. 宛先にディレクトリが存在する場合、そのディレクトリ配下に移動・コピーを行う

  * 複数のファイルやディレクトリを移動・コピー可能

2. 宛先にファイルが存在する場合、そのファイルに上書き操作を行う

  * 移動・コピー元は単一のファイルやディレクトリでなければならない
  * ``--overwrite`` オプションを指定する必要がある

3. 宛先にファイルやディレクトリが **存在せず** 、その親ディレクトリが存在する場合、宛先に単一のファイルを作成する

  * 移動・コピー元は単一のファイルやディレクトリでなければならない

4. 宛先にファイルやディレクトリが **存在せず** 、その親ディレクトリも **存在しない** 場合、エラーとなる

また、それぞれ下記の共通オプションを利用可能です。

..  program:: directio subcommand file

..  option:: -r, --recursive

    ファイルだけでなく、ディレクトリーもコピーする。

    このオプションを指定しない場合、ディレクトリーのコピーを行わずスキップする。

    :program:`directio move` においては常にディレクトリーの移動を行うため、このオプションは利用できない。

    ディレクトリーを移動・コピーする際に宛先にすでにディレクトリーが存在する場合、コピー元のディレクトリーの内容を宛先にマージする。

..  option:: -w, --overwrite

    宛先にすでにファイルが存在した場合、そのファイルを上書きする。

    このオプションを指定せずに、ファイルを上書きしようとした場合エラーとなる。

..  option:: -p, --parallel

    複数ファイルの操作を並列に実行する。

.. _`directio-cmd-list`:

:program:`directio list`
------------------------

:program:`list` はDirect I/Oのデータソースに含まれるファイルの一覧を表示します。

書式
~~~~

..  code-block:: sh

    directio list [options] [directio-path..]

使用例
~~~~~~

:program:`list` を標準のオプションで実行すると、Direct I/Oのすべてのデータソースに含まれるファイルやディレクトリーのパス一覧を表示します。

..  code-block:: sh

    $ directio list
    file:/home/asakusa/target/testing/directio/master
    file:/home/asakusa/target/testing/directio/master/item_info.csv
    file:/home/asakusa/target/testing/directio/master/store_info.csv
    file:/home/asakusa/target/testing/directio/result
    file:/home/asakusa/target/testing/directio/result/category
    file:/home/asakusa/target/testing/directio/result/category/result.csv
    file:/home/asakusa/target/testing/directio/result/error
    file:/home/asakusa/target/testing/directio/result/error/2011-04-01.csv
    file:/home/asakusa/target/testing/directio/sales
    file:/home/asakusa/target/testing/directio/sales/2011-04-01.csv

:program:`list` のオプションには表示するファイル名のパターンを指定することができます。

..  code-block:: sh

    $ directio list "result/**/*"
    file:/home/asakusa/target/testing/directio/result/category
    file:/home/asakusa/target/testing/directio/result/category/result.csv
    file:/home/asakusa/target/testing/directio/result/error
    file:/home/asakusa/target/testing/directio/result/error/2011-04-01.csv

:program:`list` を詳細オプション付きで実行すると、ファイルに付随する属性情報も表示します。

..  code-block:: sh

    $ directio list -v "result/**/*"
    total 4
    file:/home/asakusa/target/testing/directio/result/category
        data source: root
          directory: true
    file:/home/asakusa/target/testing/directio/result/category/result.csv
        data source: root
          directory: false
    file:/home/asakusa/target/testing/directio/result/error
        data source: root
          directory: true
    file:/home/asakusa/target/testing/directio/result/error/2011-04-01.csv
        data source: root
          directory: false

.. _`directio-cmd-mkdir`:

:program:`directio mkdir`
-------------------------

:program:`mkdir` はDirect I/Oのデータソース上にディレクトリを作成します。

書式
~~~~

..  code-block:: sh

    directio mkdir [options] directio-path..

使用例
~~~~~~

..  code-block:: sh

    $ directio mkdir /temp/foo

    $ directio mkdir -v /temp/foo/bar
    create directory: file:/home/asakusa/target/testing/directio/temp/foo/bar

.. _`directio-cmd-get`:

:program:`directio get`
-----------------------

:program:`get` はDirect I/Oのデータソース上のファイルをローカルファイルシステムにコピーします。

書式
~~~~

..  code-block:: sh

    directio get [options] directio-path.. local-path

使用例
~~~~~~

1つのファイルを取得する例です。

..  code-block:: sh

    $ directio get /result/category/result.csv $HOME/work

ディレクトリ配下のすべてのファイルを取得する例です。 ``-r`` オプションを指定します。

..  code-block:: sh

    $ directio get -r -v /result $HOME/work
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result -> file:/home/asakusa/work/result
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/category -> file:/home/asakusa/work/result/category
    copy file: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/category/result.csv -> file:/home/asakusa/work/result/category/result.csv
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error -> file:/home/asakusa/work/result/error
    copy file: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error/2011-04-01.csv -> file:/home/asakusa/work/result/error/2011-04-01.csv

大量のファイルを取得する場合、 ``-p`` オプションを指定して並列にファイルを取得すると全体のファイル取得時間が短縮できる可能性があります。

..  code-block:: sh

    $ directio get -r -p "/data/*" /mnt/data

.. _`directio-cmd-put`:

:program:`directio put`
-----------------------

:program:`put` はローカルファイルシステム上のファイルをDirect I/Oのデータソース上にコピーします。

書式
~~~~

..  code-block:: sh

    directio put [options] local-path.. directio-path

使用例
~~~~~~

1つのファイルをコピーする例です。 ``-w`` オプションを指定すると、すでに存在する同名のファイルを上書きします。

..  code-block:: sh

    $ directio put -w example-dataset/sales/2011-04-01.csv /sales

ディレクトリ配下のすべてのファイルをコピーする例です。 ``-r`` オプションを指定します。

..  code-block:: sh

    $ directio put -r -v $ASAKUSA_HOME/example-dataset/* /
    copy directory: file:/home/asakusa/asakusa/example-dataset/master -> hdfs://<host>:8020/user/asakusa/target/testing/directio/master
    copy file: file:/home/asakusa/asakusa/example-dataset/master/item_info.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/master/item_info.csv
    copy file: file:/home/asakusa/asakusa/example-dataset/master/store_info.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/master/store_info.csv
    copy directory: file:/home/asakusa/asakusa/example-dataset/sales -> hdfs://<host>:8020/user/asakusa/target/testing/directio/sales
    copy file: file:/home/asakusa/asakusa/example-dataset/sales/2011-04-01.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/sales/2011-04-01.csv

大量のファイルをコピーする場合、 ``-p`` オプションを指定して並列にファイルをコピーすると全体のファイル取得時間が短縮できる可能性があります。

..  code-block:: sh

    $ directio put -r -p /mnt/data/* /data

.. _`directio-cmd-delete`:

:program:`directio delete`
--------------------------

:program:`delete` はDirect I/Oのデータソース上のファイルを削除します。

書式
~~~~

..  code-block:: sh

    directio delete [options] directio-path..

使用例
~~~~~~

1つのファイルを削除する例です。

..  code-block:: sh

    $ directio delete result/error/2011-04-01.csv

ディレクトリとその配下のすべてのファイルを削除する例です。 ``-r`` オプションを指定します。

..  code-block:: sh

    $ directio delete -r -v result
    delete: hdfs://<host>:8020/user/asakusa/target/testing/directio/result

データソース上のファイルをすべて削除する例です。

..  code-block:: sh

    $ directio delete -r "/*"

..  attention::

    先述の `directio-path`_ にも記載していますが、ファイル名にワイルドカードを含むパターンを指定する場合、
    利用するシェルによって意図せず展開されないよう ``"/*"`` のようにダブルクウォート文字で囲むなどの指定を行なってください。

.. _`directio-cmd-copy`:

:program:`directio copy`
------------------------

:program:`copy` はDirect I/Oのデータソース間でファイルをコピーします。

書式
~~~~

..  code-block:: sh

    $ directio copy [options] source-directio-path.. destination-directio-path

使用例
~~~~~~

1つのファイルをコピーする例です。

..  code-block:: sh

    $ directio copy /result/category/result.csv /temp/result_bak.csv

ディレクトリとその配下のすべてのファイルをコピーする例です。 ``-r`` オプションを指定します。

..  code-block:: sh

    $ directio copy -r -v /result /result_bak
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/category -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/category
    copy file: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/category/result.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/category/result.csv
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/error
    copy file: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error/2011-04-01.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/error/2011-04-01.csv

大量のファイルをコピーする場合、 ``-p`` オプションを指定して並列にファイルをコピーすると全体のファイル取得時間が短縮できる可能性があります。

..  code-block:: sh

    $ directio put -r -p /data /work

.. _`directio-cmd-move`:

:program:`directio move`
------------------------

:program:`move` はDirect I/Oのデータソース間でファイルを移動します。

書式
~~~~

..  code-block:: sh

    $ directio move [options] source-directio-path.. destination-directio-path

使用例
~~~~~~

1つのファイルを別ディレクトリに移動する例です。

..  code-block:: sh

    $ directio move /result/category/result.csv /temp

ディレクトリとその配下のすべてのファイルを移動する例です。

..  code-block:: sh

    $ directio move -v /result /result_bak
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/category -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/category
    copy directory: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/error
    copy file: hdfs://<host>:8020/user/asakusa/target/testing/directio/result/error/2011-04-01.csv -> hdfs://<host>:8020/user/asakusa/target/testing/directio/result_bak/error/2011-04-01.csv

.. _`directio-cmd-configuration`:

:program:`directio configuration`
---------------------------------

:program:`configuration` は、環境上のDirect I/Oの設定に関する情報を表示します。
:program:`configuration` のサブコマンド一覧を以下に示します。

..  list-table:: :program:`configuration` サブコマンド
    :widths: 5 5
    :header-rows: 1

    * - サブコマンド
      - 説明
    * - :ref:`directio-cmd-configuration-list`
      - データソースの一覧を表示する
    * - :ref:`directio-cmd-configuration-system`
      - システム設定の一覧を表示する。

.. _`directio-cmd-configuration-list`:

:program:`directio configuration list`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`list` は環境上のDirect I/Oに定義されているデータソースの一覧を表示します。

書式
~~~~

..  code-block:: sh

    directio configuration list [options] [data-source-ID]

使用例
~~~~~~

:program:`list` を標準のオプションで実行すると、Direct I/OのデータソースID一覧を表示します。

..  code-block:: sh

    $ directio configuration list
    root
    s3

:program:`list` を詳細オプション付きで実行すると、各データソースの設定情報 [#]_ も表示します。

..  code-block:: sh

    $ directio configuration list -v
    total 2
    root
        ID: root
        base-path: /
        class: com.asakusafw.runtime.directio.hadoop.HadoopDataSource
        attributes:
        - fs.path: target/testing/directio
    s3
        ID: s3
        base-path: s3/spool
        class: com.asakusafw.runtime.directio.hadoop.HadoopDataSource
        attributes:
        - fs.path: s3://example/var/spool
        - output.staging: false

..  [#] Direct I/Oのデータソース設定については、 :doc:`../directio/user-guide` - データソースの設定 を参照してください。

.. _`directio-cmd-configuration-system`:

:program:`directio configuration system`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`system` は環境上のDirect I/Oのシステム設定 [#]_ に関する情報を表示します。

書式
~~~~

..  code-block:: sh

    directio configuration system [options]

使用例
~~~~~~

..  code-block:: sh

    $ directio configuration system
    configuration: /home/asakusa/asakusa/core/conf/asakusa-resources.xml
    system directory: file:/home/asakusa/_directio
    local temporary: N/A

..  [#] Direct I/Oのシステム設定については、 :doc:`../directio/user-guide` - その他の設定 を参照してください。

.. _`directio-cmd-transaction`:

:program:`directio transaction`
-------------------------------

:program:`transaction` は、Direct I/Oのトランザクション操作 [#]_ を行います。
:program:`transaction` のサブコマンド一覧を以下に示します。

..  list-table:: :program:`transaction` サブコマンド
    :widths: 3 7
    :header-rows: 1

    * - サブコマンド
      - 説明
    * - :ref:`directio-cmd-transaction-list`
      - Direct I/Oのトランザクションの一覧を表示する
    * - :ref:`directio-cmd-transaction-show`
      - Direct I/Oのトランザクションの詳細情報を表示する
    * - :ref:`directio-cmd-transaction-apply`
      - Direct I/Oでコミットに成功した未適用のトランザクションを適用する
    * - :ref:`directio-cmd-transaction-abort`
      - Direct I/Oのトランザクションを破棄する

..  [#] Direct I/Oのトランザクション制御については :doc:`user-guide` を参照してください。

.. _`directio-cmd-transaction-list`:

:program:`directio transaction list`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`list` はDirect I/Oのトランザクションの一覧を表示します。

書式
~~~~

..  code-block:: sh

    $ directio transaction list [options]

使用例
~~~~~~

実行中のDirect I/Oトランザクションが存在しない場合は、以下のように表示されます。

..  code-block:: sh

    $ directio transaction list
    17/11/07 17:11:29 INFO hadoop.DirectIoTransactionEditor: Start listing Direct I/O transactions
    17/11/07 17:11:29 INFO hadoop.DirectIoTransactionEditor: There are no Direct I/O transactions

実行中のDirect I/Oトランザクションが存在する場合は、以下のように表示されます。
詳細オプション付きで実行すると、トランザクションに関する詳細な情報が表示されます。

..  code-block:: sh

    $ directio transaction list -v
    17/11/07 17:19:01 INFO hadoop.DirectIoTransactionEditor: Start listing Direct I/O transactions
    17/11/07 17:19:02 INFO hadoop.DirectIoTransactionEditor: Start extracting 1 Direct I/O commit information
    17/11/07 17:19:02 INFO hadoop.DirectIoTransactionEditor: Finish listing Direct I/O transactions
    c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
        ID: c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
        status: Committed
        date: 2017-11-07T08:18:33Z
        comment:
        > User Name: asakusa
        > Batch ID: m3bp.perf.average.cogsort.once
        > Flow ID: cogsort_once
        > Execution ID: c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
        > Batch Arguments: {input=10G/input, output=10G/output}

.. _`directio-cmd-transaction-show`:

:program:`directio transaction show`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`show` はDirect I/Oのトランザクションの詳細情報を表示します。

コマンドのパラメータには :program:`list` で表示した実行IDを指定します。

書式
~~~~

..  code-block:: sh

    $ directio transaction show [options] execution-ID

使用例
~~~~~~

..  code-block:: sh

    $ directio transaction show c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
    ID: c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
    status: Committed
    date: 2017-11-07T08:18:33Z
    comment:
    > User Name: asakusa
    > Batch ID: m3bp.perf.average.cogsort.once
    > Flow ID: cogsort_once
    > Execution ID: c09f4137-5d0b-4c9c-8bee-69eb05c13bc8
    > Batch Arguments: {input=10G/input, output=10G/output}

.. _`directio-cmd-transaction-apply`:

:program:`directio transaction apply`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`apply` はDirect I/Oでコミットに成功した未適用のトランザクションを、最後まで適用します。
この操作によって、in-doubt状態になっているトランザクションを適切に終了させることができます。

コマンドのパラメータには :program:`list` で表示した実行IDを指定します。
:program:`list` や :program:`show` で表示される ``status`` の項目が ``Committed`` となっているもののみを、このコマンドで処理できます。
``status`` の項目が ``Committed`` でない場合、このコマンドを実行するとエラーとなります。

書式
~~~~

..  code-block:: sh

    $ directio transaction apply [options] execution-ID

使用例
~~~~~~

..  code-block:: sh

    $ directio transaction apply -v 3819e025-4472-447f-9cf5-bd2df2507337
    apply transaction
    ID: 3819e025-4472-447f-9cf5-bd2df2507337
    status: Committed
    date: 2017-11-08T07:42:15Z
    comment:
    > User Name: asakusa
    > Batch ID: m3bp.perf.average.cogsort.once
    > Flow ID: cogsort_once
    > Execution ID: 3819e025-4472-447f-9cf5-bd2df2507337
    > Batch Arguments: {input=1G/input, output=1G/output}
    17/11/08 16:46:28 INFO hadoop.DirectIoTransactionEditor: Start applying Direct I/O transaction (executionId=3819e025-4472-447f-9cf5-bd2df2507337)
    17/11/08 16:46:28 INFO hadoop.DirectIoTransactionEditor: Start initializing Direct I/O data stores
    17/11/08 16:46:28 INFO hadoop.DirectIoTransactionEditor: Finish initializing Direct I/O data stores
    17/11/08 16:46:28 INFO hadoop.DirectIoTransactionEditor: Deleting commit mark (executionId=3819e025-4472-447f-9cf5-bd2df2507337, path=file:/home/asakusa/_directio/transactions/commit-3819e025-4472-447f-9cf5-bd2df2507337)
    17/11/08 16:46:28 INFO hadoop.DirectIoTransactionEditor: Finish applying Direct I/O transaction (executionId=3819e025-4472-447f-9cf5-bd2df2507337)

.. _`directio-cmd-transaction-abort`:

:program:`directio transaction abort`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:program:`abort` はDirect I/Oで行われた任意のトランザクションを破棄します。

コマンドのパラメータには :program:`list` で表示した実行IDを指定します。

``status`` の項が ``Committed`` , ``Uncommitted`` のいずれの場合でも途中結果を強制的に破棄することができます。
``status`` の項が ``Committed`` のトランザクションを破棄する場合、 ``--force`` ( ``-f`` )  オプションを指定します。

..  warning::
    ``status`` の項目が ``Committed`` になってるトランザクションに対してこのコマンドを実行すると、処理結果が中途半端にデータソース上に反映されたまま復元できなくなる場合があります。

    そのようなトランザクションには通常 :program:`apply` によってコミットの適用を行うべきですが、コミットの内容が不要になった場合や、コミットの内容がエラーによりどうやっても適用できない場合などには、上記のコマンドも利用できます。

..  hint::
    ``status`` の項目が ``Uncommitted`` である場合、コミットの破棄はほぼロールバック操作と同様になります。
    ただし、Direct I/Oの出力時に「ステージ領域の省略」を行っていた場合には、途中結果が出力先に一部反映されている可能性があります。

書式
~~~~

..  code-block:: sh

    $ directio transaction abort [options] execution-ID

使用例
~~~~~~

..  code-block:: sh

    $ directio transaction abort -v a1b4286f-b316-4cc4-b6e6-9c49a8b723a1
    abort transaction
    ID: a1b4286f-b316-4cc4-b6e6-9c49a8b723a1
    status: Uncommitted
    date: 2017-11-08T07:47:55Z
    comment:
    > User Name: asakusa
    > Batch ID: m3bp.perf.average.cogsort.once
    > Flow ID: cogsort_once
    > Execution ID: a1b4286f-b316-4cc4-b6e6-9c49a8b723a1
    > Batch Arguments: {input=1G/input, output=1G/output}
    17/11/08 16:49:09 INFO hadoop.DirectIoTransactionEditor: Start aborting Direct I/O transaction (executionId=a1b4286f-b316-4cc4-b6e6-9c49a8b723a1)
    17/11/08 16:49:09 INFO hadoop.DirectIoTransactionEditor: Start initializing Direct I/O data stores
    17/11/08 16:49:09 INFO hadoop.DirectIoTransactionEditor: Finish initializing Direct I/O data stores
    17/11/08 16:49:09 INFO hadoop.DirectIoTransactionEditor: Deleting transaction info (executionId=a1b4286f-b316-4cc4-b6e6-9c49a8b723a1, path=file:/home/asakusa/_directio/transactions/commit-a1b4286f-b316-4cc4-b6e6-9c49a8b723a1)
    17/11/08 16:49:09 INFO hadoop.DirectIoTransactionEditor: Finish aborting Direct I/O transaction (executionId=a1b4286f-b316-4cc4-b6e6-9c49a8b723a1)
