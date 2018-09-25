==============================
テストドライバーユーザーガイド
==============================

この文書では、Asakusa Frameworkを使ったバッチアプリケーションをテストする方法について紹介します。

本書ではテストケースの実装に `JUnit`_ を利用します。

..  _`JUnit`: http://www.junit.org/

.. _testing-userguide-operator-testing:

演算子のテスト
==============

Operator DSL [#]_ を使って記述した演算子に対するテストの方法は、以下の2種類の方法が提供されています。

* `演算子クラスに対するテスト`_
* `一時的なフロー記述に対するテスト`_

..  [#] Operator DSLについて詳しくは :doc:`../dsl/user-guide` - :ref:`dsl-userguide-operator-dsl` などを参照してください。

.. _testing-userguide-operator-impl-testing:

演算子クラスに対するテスト
--------------------------

この方法は、演算子のテストを一般的なクラスに対する単体テストと同様の方法で作成します。

このテストでは、演算子クラスに記述した演算子メソッドにテストデータとして用意したデータモデルオブジェクトを渡して実行し、変更されたデータモデルオブジェクトの内容やメソッドの戻り値をJUnitのAPIなどを使って検証します。

演算子クラスは抽象クラスとして宣言しているため、テストメソッド内では演算子実装クラス（演算子クラス名の末尾に ``Impl`` を付与したクラスで、Operator DSLコンパイラが自動的に生成する）のインスタンスから演算子メソッドを呼び出します。

..  code-block:: java

    @Test
    public void testCheckShipment_shipped() {
        StockOp operator = new StockOpImpl();
        Shipment shipment = new Shipment();
        shipment.setShippedDate(new DateTime());
        shipment.setCost(100);

        ShipmentStatus actual = operator.checkShipment(shipment);

        assertThat("COSTが指定されていたらCOMPLETED",
                actual, is(ShipmentStatus.COMPLETED));
    }

以降では、演算子のテストを記述を補助するテストAPIについて説明します。

OperatorTestEnvironment
~~~~~~~~~~~~~~~~~~~~~~~

いくつかの演算子のテストには、 ``OperatorTestEnvironment`` [#]_ クラスを利用します。
このクラスはAsakusaのフレームワークAPIをテスト時にエミュレーションするためのもので、フレームワークAPIを利用する演算子をテストする場合には必須です。
その他、 ``OperatorTestEnvironment`` は演算子のテスト実装に便利なユーティリティメソッドを提供します。

``OperatorTestEnvironment`` クラスは、テストクラスの ``public`` フィールドに ``@Rule`` [#]_ という注釈を付けてインスタンス化します。

..  code-block:: java

    // 必ずpublicで宣言し、インスタンスを代入する
    @Rule
    public OperatorTestEnvironment env = new OperatorTestEnvironment();


``OperatorTestEnvironment`` 利用の一例として、演算子クラスのインスタンスを生成する ``newInstance`` の使用例を示します。
``newInstance`` は指定した演算子クラスに対する実装クラスを返します。

例えば先述のテストメソッド例に対しては、演算子クラスのインスタンス生成部分を以下のように書き換えることができます。

..  code-block:: java

    @Test
    public void testCheckShipment_shipped() {
        StockOp operator = env.newInstance(StockOp.class);
        ...

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.OperatorTestEnvironment`
..  [#] ``org.junit.Rule``

.. _operator-testing-with-result:

結果型を利用する演算子のテスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

いくつかの演算子メソッドでは、出力を表す ``Result`` [#]_ 型のオブジェクトを引数に取ります。
これを利用するメソッドのテストには、モック実装の ``MockResult`` [#]_ が便利です。

..  code-block:: java

    @Rule
    public OperatorTestEnvironment env = new OperatorTestEnvironment();

    @Test
    public void testCutoff_shortage() {
        StockOp operator = env.newInstance(StockOp.class);

        List<Stock> stocks = Arrays.asList(StockFactory.create(new DateTime(), 0, 100, 10));
        List<Shipment> shipments = Arrays.asList();
        MockResult<Stock> newStocks = env.newResult(Stock.class);
        MockResult<Shipment> newShipments = env.newResult(Shipment.class);

        operator.cutoff(stocks, shipments, newStocks, newShipments);

        assertThat(newStocks.getResults().size(), is(1));
        assertThat(newShipments.getResults().size(), is(0));
    }

..  note::
    バージョン 0.9.1 以降では、 ``MockResult`` インスタンスを生成するファクトリメソッド ``OperatorTestEnvironment#newResult`` が利用できます。
    通常はこのメソッドを使って ``MockResult`` を生成することを推奨します。

なお、結果型を引数に指定する演算子については :doc:`../dsl/operators` を参照してください。

..  [#] :asakusafw-javadoc:`com.asakusafw.runtime.core.Result`
..  [#] :asakusafw-javadoc:`com.asakusafw.runtime.testing.MockResult`

コンテキストAPIを利用する演算子のテスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テスト対象の演算子がコンテキストAPI [#]_ を利用する場合、コンテキストAPIが参照するバッチの起動引数をテスト側で指定します。

バッチ起動引数の指定は、 ``OperatorTestEnvironment`` クラスの ``setBatchArg`` メソッドで行います。
``setBatchArg`` メソッドは第一引数に変数名、第二引数に変数の値を指定します。
すべてのバッチ起動引数を指定したら、同クラスの ``reload`` メソッドで設定を有効化します。

演算子メソッドに対する操作は必ず ``reload`` メソッドの呼出し後に記述してください。

..  code-block:: java

    @Rule
    public OperatorTestEnvironment env = new OperatorTestEnvironment();

    @Test
    public void sometest() {
        env.setBatchArg("key1", "value1");
        env.setBatchArg("key2", "value2");
        ...
        env.reload();

        // ここにテストを書く
    }

..  [#] コンテキストAPIについては、 :doc:`../dsl/user-guide` - :ref:`dsl-context-api` を参照してください。

実行時プラグインを利用する演算子のテスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テスト対象の演算子で実行時プラグイン [#]_ を利用する場合、「実行時プラグイン設定ファイル」が必要になります。
これは利用する実行時プラグインや、それぞれのプラグインの設定を記述したもので、 ``OperatorTestEnvironment`` クラスをインスタンス化する際に位置を指定できます。

..  code-block:: java

    @Rule
    public OperatorTestEnvironment env =
        new OperatorTestEnvironment("conf/asakusa-test-resources.xml");

ここに指定する位置は、クラスパス上の位置です。

引数を指定せずに ``OperatorTestEnvironment`` クラスをインスタンス化した場合には、クラスパスルートの ``asakusa-resources.xml`` というファイルを利用します。
このファイルがない場合、最低限の設定のみを自動的に行います。

その他、 ``OperatorTestEnvironment`` クラスの ``configure`` メソッドを利用して個々のプラグインの設定を行うことも可能です。
``configure`` メソッドは第一引数にプロパティ名、第二引数にプロパティの値を指定します。

演算子メソッドに対する操作は必ず ``reload`` メソッドの呼出し後に記述してください。

..  code-block:: java

    @Rule
    public OperatorTestEnvironment env = new OperatorTestEnvironment(...);

    @Test
    public void sometest() {
        env.configure(
            "com.asakusafw.runtime.core.Report.Delegate",
            "com.asakusafw.runtime.core.Report$Default");
        ...
        env.reload();

        // ここにテストを書く
    }

..  [#] 実行時プラグインについては、 :doc:`../administration/deployment-runtime-plugins` を参照してください。

.. _testing-userguide-dataloader:

DataLoader
~~~~~~~~~~

演算子のいくつかは、入力データとしてデータモデルのリストを引数として受け取ります。
``DataLoader`` [#]_ クラスは以下のようなデータ形式からデータモデルオブジェクトのリストを生成するユーティリティです。

* Direct I/Oのデータフォーマットに対応するファイル (CSV, TSVファイルなど)

  * :doc:`../directio/user-guide` - :ref:`directio-create-dataformat` に記載するデータフォーマットを指定することができます。
* データ記述シート(Excelファイル)

  * テストドライバー用のデータ記述シート ( :doc:`using-excel` ) を指定することができます。
* ``Iterable`` ( ``List`` )

  * ビューAPIの入力データを ``Iterable`` や ``List`` から生成する場合に使用します。

以下は、Direct I/O CSV形式のCSVファイルを入力データとして使用するテストケースの実装例です。

..  code-block:: java

    public class CategorySummaryOperatorTest {

        @Rule
        public final OperatorTestEnvironment env = new OperatorTestEnvironment();

        @Test
        public void selectAvailableItem() {

            List<ItemInfo> candidates = env.loader(ItemInfo.class,
                    ItemInfoCsvFormat.class,
                    "item_info.csv" // (or) new File("src/test/resources/com/example/operator/item_info.csv")
            ).asList();

            CategorySummaryOperator operator = env.newInstance(CategorySummaryOperator.class);
            ItemInfo item1 = operator.selectAvailableItem(candidates, sales(1));
            ItemInfo item5 = operator.selectAvailableItem(candidates, sales(5));
            ...
        }
    }

``OperatorTestEnvironment`` の ``loader`` メソッドにデータモデルクラス、 ``DataFormat`` の実装クラス [#]_ 、テストデータのファイルパスを指定して ``DataLoader`` を取得し、 ``asList`` メソッドでデータモデルオブジェクトのリストを取り出します。

ファイルパスを ``文字列`` で指定した場合はクラスパス上から検索し、 ``File`` オブジェクトで指定した場合は引数で指定したファイルパス(相対パス指定時は通常プロジェクトルートからの相対パス)を使用します。

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.loader.DataLoader`
..  [#]  ``DataFormat`` の実装クラスの作成方法は、 :doc:`../directio/user-guide` - :ref:`directio-create-dataformat` に記載するドキュメントを参照してください

.. _testing-userguide-viewapi:

ビューAPIを使った演算子のテスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`../dsl/view-api` を使った演算子のテストでは、 ``View<T>`` や ``GroupView<T>`` に対応するデータモデルオブジェクトを `DataLoader`_ を使って生成することができます。

以下は、テストデータ定義シート(Excelファイル)からビューAPIの入力データを設定するテストケースの実装例です。

..  code-block:: java

    public class WithViewOperatorTest {

        @Rule
        public final OperatorTestEnvironment env = new OperatorTestEnvironment();

        @Test
        public void updateWithView() {
            View<Foo> fooView = env.loader(Foo.class, "with_view.xls#foo")
                    .asView();
            List<SalesDetail> salesList = env.loader(SalesDetail.class, "with_view.xls#sales")
                    .asList();

            for (SalesDetail sales : salesList) {
                env.newInstance(WithViewOperator.class).updateWithView(sales, fooView);
                ...
            }
        }

        @Test
        public void extractWithGroupView() {
            GroupView<Foo> fooView = env.loader(Foo.class, "foo.xls#group_view")
                    .group("store_code")
                    .order("id")
                    .asView();
            List<SalesDetail> salesList = env.loader(SalesDetail.class, "with_view.xls#sales")
                    .asList();
            MockResult<SalesDetail> result = env.newResult(SalesDetail.class);
            MockResult<ErrorRecord> error = env.newResult(ErrorRecord.class);

            for (SalesDetail sales : salesList) {
                env.newInstance(WithViewOperator.class).extractWithGroupView(sales, fooView, result, error);
                ...
            }
        }
    }

``View<T>`` に対応するオブジェクトを取得するには、 ``DataLoader`` に対して ``asView`` メソッドを呼び出します。

``GroupView<T>`` に対応するオブジェクトを取得するには、 ``DataLoader`` に対して ``group`` メソッドでグループを指定し、このメソッドが返す ``GroupLoader`` [#]_ に対して ``asView`` メソッドを呼び出します。

``DataLoader`` で取得するデータに対して整列順序を指定したい場合は、上例のように ``order`` メソッドに整列化キーを指定します。

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.loader.GroupLoader`

.. _testdriver-temporary-flow:

一時的なフロー記述に対するテスト
--------------------------------

この方法は、演算子のテストを `データフローのテスト`_ と同様の方法で作成します。

このテストでは、テストドライバーを使って「一時的なフロー記述」（テスト専用のデータフロー）を作成し、そのデータフローにテスト対象の演算子を含めて実行するテストケースを記述します。テストデータのセットアップや実行結果の検証はテストドライバーの機能を利用します。

この方法は `演算子クラスに対するテスト`_ と比べ、以下のようなメリットがあります。

* 複数の演算子を組み合わせたテストケースの作成が可能
* 複雑なテストデータ（入力データ、期待データ、テスト条件）を定義する様々な機能を利用可能
* 演算子とデータフローのテストを統一的な方法で記述することが可能

一時的なフロー記述を使ったテストケースの実装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一時的なフロー記述を使ったテストケースの実装方法は、基本的には後述の `データフローのテスト`_ で説明するテストドライバーを使ったデータフローのテストケースを作成する方法と同様です。以下、一時的なフロー記述を使った実装の固有部分について説明します。

データフローのテスト時には各 ``Tester`` クラスの ``runTest`` メソッドの引数に、フロー部品クラスのインスタンスやジョブフロークラス、バッチクラスのクラスオブジェクトを渡しますが、一時的なフロー記述ではFlow DSLのフロー記述メソッドと同様の形式 [#]_ で「一時的なデータフロー」を記述します。

この場合 ``runTest`` メソッドの引数は ``Runnable`` 型になります。通常は以下例のように、ラムダ式としてフロー記述メソッドの内容を記述するとよいでしょう。

..  code-block:: java

    @Test
    public void testWithTemporaryFlow() {
        // 入出力の定義
        FlowPartTester tester = new FlowPartTester(getClass());
        In<Hoge> in0 = tester.input("hoge", Hoge.class)
            .prepare("path/to/input0.xlsx");
        In<Foo> in1 = tester.input("foo", Foo.class)
            .prepare("path/to/input1.xlsx");
        Out<Bar> out = tester.output("bar", Bar.class)
            .verify(...);

        // テスト用の一時的なデータフローを構築して実行
        tester.runTest(() -> {
            HogeOperatorFactory f = new HogeOperatorFactory();
            Prepare op1 = f.prepare(in0);
            GetBars op2 = f.getBars(op1.out, in1);
            out.add(op2.out);
        });
    }

..  [#] :doc:`../dsl/user-guide` - :ref:`dsl-userguide-flow-dsl` の 「フロー記述メソッド」の項を参照

一時的なフロー記述を使ったテストのメリットとデメリット
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`一時的なフロー記述に対するテスト`_ は `演算子クラスに対するテスト`_ と比べて、一般的には以下のようなメリットやデメリットがあります。
これらの点を考慮にいれて、演算子のテスト全体の構成を検討すべきでしょう。

メリット
^^^^^^^^

* 複数の演算子を組み合わせたテストケースの作成

  メソッドの実装を書かない演算子をテストの対象に含めたい場合や、複数の演算子が組み合わさって意味をなす場合など、
  テストケースに応じた任意の単位で演算子を組み合わせてデータフローを構築して演算子を実行し、その結果を評価することができます。

  複数の演算子を組み合わせて大きな演算子を構築する、という仕組みはAsakusa DSLでは「フロー部品」の構築として提供していますが、
  フロー部品とは違った観点や粒度で演算子をテストしたいといった場合にも、この機能を利用することができます。

* 複雑なテストデータ（入力データ、期待データ、テスト条件）を持つテストケースの作成

  テストドライバーには複雑なテストデータを定義する機能が豊富に提供されており、これらを利用することで効率良くテストケースを記述することが可能となります。

* 演算子とデータフローのテストを統一的な方法で記述

  Asakusa DSLの各コンポーネントのテストをテストドライバーを利用したテストケースの記述に統一することで、テストケースの作成や管理が効率的になる可能性があります。

デメリット
^^^^^^^^^^

* テストケースの実装コスト

  特にシンプルな演算子のテストケースを記述する場合は `演算子クラスに対するテスト`_ に比べてテストケースの実装コストが高いでしょう。

* テスト実行速度とマシンリソースへの負荷

  テストドライバーの実行時には、テストケースに定義したデータフローから実行形式へのコンパイル、入出力データのセットアップなどの処理が行われます。
  このため、多くの場合 `演算子クラスに対するテスト`_ に比べてテストケースの実行に時間がかかり、マシンへの負荷は高くなるでしょう。

.. _testing-userguide-dataflow-testing:

データフローのテスト
====================

Flow DSL [#]_ を使って記述したデータフロー、およびBatch DSL [#]_ を使って記述したバッチに対するテストでは、DSLのコンパイラや実行環境と連携してテストを実行します。

Asakusa Frameworkはこの一連の処理を自動的に行うテストドライバーというモジュールを含んでいます。

テストドライバーはテスト対象の要素に対して、次の一連の処理を行います。

#. 入力データを初期化する
#. 入力データを流し込む
#. 対象のプログラムをテスト用の実行エンジン向けにDSLコンパイルする
#. 対象のプログラムを実行する
#. 出力結果を取り込む
#. 出力結果と期待データを検証する

..  [#] Flow DSLについて詳しくは :doc:`../dsl/user-guide` - :ref:`dsl-userguide-flow-dsl` などを参照してください。
..  [#] Batch DSLについて詳しくは :doc:`../dsl/user-guide` - :ref:`dsl-userguide-batch-dsl` などを参照してください。

テストデータの準備
------------------

テストドライバーでのテストを行うには、次の3種類の情報を用意します。
これらをまとめて「テストデータ」と呼ぶことにします。

入力データ
  それぞれのデータフローの入力に指定するデータセット。
  データモデルオブジェクトのリストと同じ構造。

期待データ
  それぞれのデータフローからの出力に期待するデータセット。
  入力データと同じ構造。

テスト条件
  それぞれの出力と期待データを比較して間違いを見つける方法。

テストドライバーはテストデータをさまざまな形式で記述できます。
詳細は後述の `テストデータの作成`_ にて説明します。

ここでは初めて利用する際に理解のしやすい `Excelファイル形式`_ での準備方法を紹介します。

テストデータテンプレートの生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テストデータをExcelで記述する場合、そのテンプレートを自動生成して利用します。
このテンプレートはデータモデルごとに生成され、それぞれ次のようなシートが含まれます。

入力データシート
  入力データを記述するシート。
  データモデルをシートの1行で表し、カラムごとにプロパティの値を記載できる。
  テンプレートではプロパティ名のヘッダのみが記載されている。

  ..  figure:: shipment-input.png

      [入力データシートの例]

期待データシート
  期待する出力データを記述するシート。
  入力データシートと同じ構造。

比較条件シート
  出力結果データと期待データの比較条件を記述するシート。
  それぞれのプロパティをどのように比較するかをドロップダウン形式で選択できる。

  ..  figure:: shipment-rule.png

      [比較条件シートの例]

テストデータのテンプレートを生成するには、 Gradleを利用してテストデータテンプレート生成ツールを実行します。
これはGradleの :program:`generateTestbook` タスクで起動するので、プロジェクト内で以下のようにコマンドを実行します。

..  code-block:: sh

    ./gradlew generateTestbook

このコマンドを実行すると、プロジェクトの :file:`build/excel` 配下に、DMDLで記述したそれぞれのデータモデルごとExcelのファイルが生成されます。
このファイルには、上記の3種類のシートが含められます。

なお、このテンプレートはDMDLで記述されたデータモデルを元に作成しています。
DMDLの利用方法は :doc:`../dmdl/start-guide` を参照してください。

入力、期待データの作成
~~~~~~~~~~~~~~~~~~~~~~

入力データを作成するには、生成したExcelファイルの ``input`` という名前のシートを編集します。
このシートの1行目には、データモデルに定義したプロパティの名前が記載されているはずです。
それぞれの行にオブジェクトごとのプロパティを入力してください。

期待データを作成するには、同様に ``output`` という名前のシートを編集して下さい。

..  attention::
    セルを空にした場合、その値は ``null`` として取り扱われます。

..  attention::
    文字列型のプロパティを編集する際には注意が必要です。
    数値、日付、論理値などの値を指定したセルや、空のセルは文字列として取り扱われません。
    これらの値を利用したい場合には、セルを ``'`` から始めて文字列を指定してください。
    また、長さ0の文字列を入力したい場合には ``'`` のみを指定してください。

テスト条件の記述
~~~~~~~~~~~~~~~~

Excelファイルのテストデータテンプレートを利用する場合、出力データと期待データは次のように比較されます。

#. 各レコードのキーとなるプロパティをもとに、出力データと期待データのペアを作る
#. 出力と期待データのペアの中で、プロパティを条件に従って比較する
#. ペアを作れなかった出力データまたは期待データは、条件に従って比較する

上記の 1)キープロパティ、 2)プロパティの比較、 3)全体の比較 はそれぞれ生成したExcelファイルの ``rule`` という名前のシートで指定できます。

レコードのキーを指定する場合には、対象プロパティの「値の比較」という項目に ``検査キー[Key]`` を選択します。
キーとならないプロパティは、「値の比較」や「NULLの比較」にそれぞれ比較の条件を選択してください。

プロパティを比較しない場合には、「値の比較」に ``検査対象外[-]`` を、「NULLの比較」に ``通常比較[-]`` をそれぞれ選択します。

出力と期待データのペアを作れなかった場合の動作は、シート上部の「全体の比較」で選択します。

Excelファイルの配置
~~~~~~~~~~~~~~~~~~~

作成したExcelファイルは、クラスパスが通っているファイルパス上に配置します。

:doc:`../introduction/start-guide` で作成したプロジェクトの構成では、 :file:`src/test/resources/<パッケージ>` 以下にExcelファイル配置することを推奨します。

通常は `テストクラスの作成`_ で作成するテストクラスと同じパッケージ上に配置するとよいでしょう。

テストクラスの作成
------------------

テストケースを記述するテストクラスを作成します。

:doc:`../introduction/start-guide` で作成したプロジェクトの構成では、 :file:`src/test/java/<パッケージ>` 以下にクラスファイルを配置することを推奨します。

通常は `Excelファイルの配置`_ で配置するExcelファイルのパスと同じパッケージ上に配置するとよいでしょう。

フロー部品のテスト
------------------

フロー部品をテストするには、 ``FlowPartTester`` [#]_ を利用します。

..  code-block:: java

    @Test
    public void testExampleAsFlowPart() {
        FlowPartTester tester = new FlowPartTester(getClass());
        In<Shipment> shipmentIn = tester.input("shipment", Shipment.class)
            .prepare("shipment.xls#input");
        In<Stock> stockIn = tester.input("stock", Stock.class)
            .prepare("stock.xls#input");
        Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
            .verify("shipment.xls#output", "shipment.xls#rule");
        Out<Stock> stockOut = tester.output("stock", Stock.class)
            .verify("stock.xls#output", "stock.xls#rule");

        FlowDescription flowPart = new StockJob(shipmentIn, stockIn, shipmentOut, stockOut);
        tester.runTest(flowPart);
    }

``FlowPartTester`` をインスタンス化する際には、引数に ``getClass()`` を指定してテストケース自身のクラスを引き渡します。
これは、先ほど配置したテストデータを検索するなどに利用しています。

..  code-block:: java

    FlowPartTester tester = new FlowPartTester(getClass());

データフローの入力を定義するには、 ``input`` メソッドを利用します。
この引数には入力の名前 [#]_ と、入力のデータモデル型を指定します。

``input`` に続けて、 ``prepare`` [#]_ で入力データを指定します。
`Excelファイル形式`_ の入力データシートを利用する場合は、入力データを定義したExcelシートのパスを以下のいずれかで指定します。

* パッケージからの相対パス
* クラスパスからの絶対パス ( ``/`` から始める )

上記の一連の結果を、 ``In<データモデル型>`` [#]_ の変数に保持します。

..  code-block:: java

    In<Shipment> shipmentIn = tester.input("shipment", Shipment.class)
        .prepare("shipment.xls#input");
    In<Stock> stockIn = tester.input("stock", Stock.class)
        .prepare("stock.xls#input");

データフローの出力を定義するには、 ``output`` メソッドを利用します。
この引数は入力と同様に名前とデータモデル型を指定します。

``output`` に続けて、 ``verify`` [#]_ で期待データとテスト条件をそれぞれ指定します。
指定方法は入力データと同様です。

出力の定義結果は、 ``Out<データモデル型>`` [#]_ の変数に保存します。

..  code-block:: java

    Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
        .verify("shipment.xls#output", "shipment.xls#rule");
    Out<Stock> stockOut = tester.output("stock", Stock.class)
        .verify("stock.xls#output", "stock.xls#rule");

入出力の定義が終わったら、フロー部品クラスを直接インスタンス化します。
このときの引数には、先ほど作成した ``In<データモデル型>`` と ``Out<データモデル型>`` を利用してください。
このインスタンスを ``runTest`` メソッドに渡すと、テストデータに応じたテストを自動的に実行します。

..  code-block:: java

    In<Shipment> shipmentIn = ...;
    In<Stock> stockIn = ...;
    Out<Shipment> shipmentOut = ...;
    Out<Stock> stockOut = ...;
    FlowDescription flowPart = new StockJob(shipmentIn, stockIn, shipmentOut, stockOut);
    tester.runTest(flowPart);

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.FlowPartTester`
..  [#] ここの名前は他の名前と重複せず、アルファベットや数字のみで構成して下さい
..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.FlowDriverInput`
..  [#] :asakusafw-javadoc:`com.asakusafw.vocabulary.flow.In`
..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.FlowDriverOutput`
..  [#] :asakusafw-javadoc:`com.asakusafw.vocabulary.flow.Out`

ジョブフローのテスト
--------------------

ジョブフローをテストするには、 ``JobFlowTester`` [#]_ を利用します。

..  code-block:: java

    @Test
    public void testExample() {
        JobFlowTester tester = new JobFlowTester(getClass());
        tester.input("shipment", Shipment.class)
            .prepare("shipment.xls#input");
        tester.input("stock", Stock.class)
            .prepare("stock.xls#input");
        tester.output("shipment", Shipment.class)
            .verify("shipment.xls#output", "shipment.xls#rule");
        tester.output("stock", Stock.class)
            .verify("stock.xls#output", "stock.xls#rule");
        tester.runTest(StockJob.class);
    }

利用方法は `フロー部品のテスト`_ とほぼ同様ですが、以下の点が異なります。

* 入出力の名前には、ジョブフローの注釈 ``Import`` や ``Export`` の ``name`` に指定した値を利用する
* 入出力を ``In`` や ``Out`` に保持しない
* ``runTest`` メソッドにはジョブフロークラス( ``.class`` )を指定する

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.JobFlowTester`

FlowPartTesterを使ったジョブフローのテスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``JobFlowTester`` を利用する場合、テスト実行時にジョブフローに定義しているインポータ記述、エクスポータ記述に基づいた外部連携モジュールが動作します。

この動作は外部システムと連携したテストを行うことができる一方で、テストドライバー実行環境に外部連携モジュールと接続する外部システムの設定が必要となります。例えばジョブフローがWindGate JDBCを利用する場合、WindGateが接続するデータベースの環境設定が必要になります。

ジョブフローのテストを行いたいが、外部連携モジュールとは接続せずにフロー記述メソッドの内容のみを検証したい、という場合があります。
このような場合、 `フロー部品のテスト`_ で利用した ``FlowPartTester`` を使ってジョブフローのテストを行うこともできます。

``FlowPartTester`` を使うことでテスト実行時のみジョブフローをフロー部品のように取り扱い、外部連携モジュールとの接続を行わずフロー記述メソッド部分のみを検証することができます。

バッチのテスト
--------------

バッチをテストするには、 ``BatchTester`` [#]_ を利用します。

..  code-block:: java

    @Test
    public void testExample() {
        BatchTester tester = new BatchTester(getClass());
        tester.jobflow("stock").input("shipment", Shipment.class)
            .prepare("shipment.xls#input");
        tester.jobflow("stock").input("stock", Stock.class)
            .prepare("stock.xls#input");
        tester.jobflow("stock").output("shipment", Shipment.class)
            .verify("shipment.xls#output", "shipment.xls#rule");
        tester.jobflow("stock").output("stock", Stock.class)
            .verify("stock.xls#output", "stock.xls#rule");
        tester.runTest(StockBatch.class);
    }

利用方法は `ジョブフローのテスト`_ とほぼ同様ですが、以下の点が異なります。

* 入出力を指定する前に、 ``jobflow`` メソッドを経由して入出力を利用するジョブフローのID [#]_ を指定する
* ``runTest`` メソッドにはバッチクラス( ``.class`` )を指定する

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.BatchTester`
..  [#] 注釈 ``@JobFlow`` の ``name`` に指定した文字列を利用して下さい

.. _testing-userguide-testdata:

テストデータの作成
==================

テストドライバーがサポートしているテストデータの形式には以下のようなものがあります。

* `Excelファイル形式`_
* `JSONファイル形式`_
* `Direct I/Oファイル形式`_ ( CSV, TSVファイルなど )
* `Javaクラス(オブジェクト)`_

テストデータの配置
------------------

`Excelファイル形式`_ 、 `JSONファイル形式`_ 、`Direct I/Oファイル形式`_ で作成するテストデータ用のファイルは、クラスパスが通っているファイルパス上に配置します。
通常はテストクラスと同じパッケージか、そのサブパッケージ上に配置します。

:doc:`../introduction/start-guide` などの手順でプロジェクトテンプレートから作成したプロジェクトでは ``src/test/resources`` 配下にファイルを配置することを推奨しています。

複数のテストから利用されるテストデータを、任意のパッケージに配置することもできます。
この場合テストデータの指定時に、クラスパスからの絶対パスを指定する必要があります。

Excelファイル形式
-----------------

Asakusa FrameworkではExcelファイル形式でテストデータを定義するための、以下のようなツールを提供しています。

* DMDLスクリプトのデータモデル定義に対応する、テストデータ定義用のテンプレートを生成するコマンドラインツール
* Excelシート上にデータフローの入力データ、期待データを定義するデータ記述シート
* Excelシート上に詳細なテスト条件（出力結果データと期待データの比較条件）を定義する比較条件シート

これらの基本的な使い方については、先述の `テストデータの準備`_ を参考にしてください。
各ツールの詳細は、以下のドキュメントを参照してください。

* :doc:`using-excel`

Excelファイルをテストドライバーで使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

作成したExcelファイルをテストドライバーで使用するには、 各 ``Tester`` クラスの ``input.prepare()`` メソッドや ``output.verify()`` メソッドの各引数に、 ``<ファイルパス>#<シート名>`` を指定します。

..  code-block:: java

    In<Shipment> shipmentIn = tester.input("shipment", Shipment.class)
        .prepare("shipment.xls#input");
    In<Stock> stockIn = tester.input("stock", Stock.class)
        .prepare("stock.xls#input");

..  code-block:: java

    Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
        .verify("shipment.xls#output", "shipment.xls#rule");
    Out<Stock> stockOut = tester.output("stock", Stock.class)
        .verify("stock.xls#output", "stock.xls#rule");

* テストクラスと同じパッケージにExcelファイルを配置した場合は、ファイルパス部分はファイル名のみを指定します。
* サブパッケージ ``a.b`` などに配置した場合には、 ``a/b/file.xls#hoge`` のようにパスを ``/`` で区切って指定します。
* 複数のテストから共通のテストデータとして利用する目的などで、任意のパッケージ上に配置した場合は、``/x/y/file.xls#fuga`` のようにパスの先頭に ``/`` から始まるパスを指定します。

JSONファイル形式
----------------

入力データと期待データを、JSONファイルを読み込んで生成することができます。

現在のところ、JSON形式でテスト条件を記述することはできません。
`Excelファイル形式`_ の比較条件シートを使用するか、`Javaクラス(オブジェクト)`_ で説明する方法でテスト条件を定義してください。

JSON形式によるテストデータ定義の詳細は、以下のドキュメントを参照してください。

* :doc:`using-json`

JSONファイルをテストドライバーで使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

作成したJSONファイルをテストドライバーで使用するには、 各 ``Tester`` クラスの ``input.prepare()`` メソッドや ``output.verify()`` メソッドの各引数に、 ``<ファイルパス>`` を指定します。

ただし、テスト条件はJSONファイルで定義することができないので、他の形式で作成したファイルなどを指定します。

..  code-block:: java

    In<Shipment> shipmentIn = tester.input("shipment", Shipment.class)
        .prepare("shipment_input.json");
    In<Stock> stockIn = tester.input("stock", Stock.class)
        .prepare("stock_input.json");

..  code-block:: java

    Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
        .verify("shipment_output.json", "shipment.xls#rule");
    Out<Stock> stockOut = tester.output("stock", Stock.class)
        .verify("stock_output.json", "stock.xls#rule");

その他、ファイルパスの指定方法は `Excelファイルをテストドライバーで使用する`_ と同様です。

.. _testing-userguide-testdata-directio:

Direct I/Oファイル形式
----------------------

入力データと期待データを、Direct I/Oが取り扱うことができるフォーマットファイルを読み込んで生成することができます。

この機能を使うことで、CSV形式やTSV形式など、Direct I/Oが対応する様々なフォーマットファイルをテストデータとして利用することが可能になります。

現在のところ、Direct I/Oファイル形式でテスト条件を記述することはできません。
`Excelファイル形式`_ の比較条件シートを使用するか、`Javaクラス(オブジェクト)`_ で説明する方法でテスト条件を定義してください。

Direct I/Oファイルをテストドライバーで使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

作成したDirect I/Oファイルをテストドライバーで使用するには、 各 ``Tester`` クラスの ``input.prepare()`` メソッドや ``output.verify()`` メソッドの各引数に、 ``DataFormat`` の実装クラス [#]_ と ``<ファイルパス>`` を指定します。

ただし、テスト条件はDirect I/Oファイルで定義することができないので、他の形式で作成したファイルなどを指定します。

以下は、Direct I/O CSV 形式のCSVファイルを入力データ、期待データに指定する実装例です。

..  code-block:: java

    tester.input("storeInfo", StoreInfo.class).prepare(
            StoreInfoCsvFormat.class,
            "store_info.csv");
    tester.input("itemInfo", ItemInfo.class).prepare(
            ItemInfoCsvFormat.class,
            "item_info.csv");
    tester.input("salesDetail", SalesDetail.class).prepare(
            SalesDetailCsvFormat.class,
            new File("src/test/resources/com/example/jobflow/2011-04-01.csv"));

..  code-block:: java

    tester.output("categorySummary", CategorySummary.class).verify(
            CategorySummaryCsvFormat.class,
            "result.csv",
            "summarize.xls#result_rule");
    tester.output("errorRecord", ErrorRecord.class).verify(
            ErrorRecordCsvFormat.class,
            "error/2011-04-01.csv",
            "error.xls#result_rule");

ファイルパスを ``文字列`` で指定した場合はクラスパス上から検索し、 ``File`` オブジェクトで指定した場合は引数で指定したファイルパス(相対パス指定時は通常プロジェクトルートからの相対パス)を使用します。

..  [#]  ``DataFormat`` の実装クラスの作成方法は、 :doc:`../directio/user-guide` - :ref:`directio-create-dataformat` に記載するドキュメントを参照してください

入出力データの変換
------------------

..  experimental::
    Asakusa Framework バージョン |version| では、入出力データの変換機能は試験的機能として提供しています。

各 ``Tester`` クラスの ``input.prepare()`` メソッドや ``output.verify()`` メソッドで指定するテストデータファイルから入出力データを構築する際に、そのデータモデルの内容を変換する処理を挿入することができます。

入力データに対してこの変換処理を適用するには ``prepare`` メソッドの第二引数( `Direct I/Oファイルをテストドライバーで使用する`_ を使う場合は第三引数)に、期待データに対して変換処理を適用するには ``verify`` に続いて ``transform`` メソッドに変換ロジックを記述したラムダ式を指定します。

..  code-block:: java

    In<Hoge> inHoge = tester.input("inHoge", Hoge.class).prepare(
            "hoge.xls#sum_in",
            hoge -> hoge.setFoo(hoge.getFoo() + 1)
    );
    Out<Hoge> outHoge = tester.output("outHoge", Hoge.class).verify(
            "hoge.xls#sum_out",
            "hoge.xls#rule"
            ).transform(hoge -> hoge.setBarAsString("test")
    );

Javaクラス(オブジェクト)
------------------------

ここではテストデータをJavaで記述する方法について紹介します。

入力データと期待データをJavaで記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

入力データや期待データをJavaで定義するには、テストドライバーAPIの ``input.prepare()`` メソッドや ``output.verify()`` メソッドでテスト対象となるデータモデル型のデータモデルオブジェクトを保持するコレクション( ``Iterable<データモデル型>`` )を指定します。

..  code-block:: java

    List<Shipment> shipments = new ArrayList<Shipment>();

    Shipment ship1 = new Shipment();
    ship1.setItemCode(1001);
    ship1.setShippedDate(DateTime.valueOf("20110102000000", Format.SIMPLE));
    shipments.add(ship1)

    Shipment ship2 = new Shipment();
    ship2.setItemCode(1002);
    ship2.setShippedDate(DateTime.valueOf("20110103000000", Format.SIMPLE));
    shipments.add(ship2)

    In<Shipment> shipmentIn = tester.input("shipment", Shipment.class)
        .prepare(shipments);

テスト条件をJavaで記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~

テスト条件は期待データと実際の結果を突き合わせるためのルールを示したもので、Javaで直接記述することも可能です。

テスト条件をJavaで記述するには、 ``ModelVerifier`` [#]_ インターフェースを実装したクラスを作成します。
このインターフェースには、2つのインターフェースメソッドが定義されています。

``Object getKey(T target)``
    指定のオブジェクトから突き合わせるためのキーを作成して返す。
    キーは ``Object.equals()`` を利用して突き合わせるため、返すオブジェクトは同メソッドを正しく実装している必要がある。

``Object verify(T expected, T actual)``
    突き合わせた2つのオブジェクトを比較し、比較に失敗した場合にはその旨のメッセージを返す。成功した場合には ``null`` を返す。

``ModelVerifier`` インターフェースを利用したテストでは、次のように期待データと結果の比較を行います。

#. それぞれの期待データから ``getKey(期待データ)`` でキーの一覧を取得する
#. それぞれの結果データから ``getKey(結果データ)`` でキーの一覧を取得する
#. 期待データと結果データから同じキーになるものを探す

   #. 見つかれば ``veriry(期待データ, 結果データ)`` を実行する
   #. 期待データに対する結果データが見つからなければ、 ``verify(期待データ, null)`` を実行する
   #. 結果データに対する期待データが見つからなければ、 ``verify(null, 結果データ)`` を実行する

#. いずれかの ``verify()`` が ``null`` 以外を返したらテストは失敗となる
#. 全ての ``verify()`` が ``null`` を返したら、次の出力に対する期待データと結果データを比較する

以下は ``ModelVerifier`` インターフェースの実装例です。
`category`, `number` という2つのプロパティから複合キーを作成して、突き合わせた結果の `value` を比較しています。
また、期待データと結果データの個数が違う場合はエラーにしています。

..  code-block:: java

    class ExampleVerifier implements ModelVerifier<Hoge> {
        @Override
        public Object getKey(Hoge target) {
            return Arrays.asList(target.getCategory(), target.getNumber());
        }

        @Override
        public Object verify(Hoge expected, Hoge actual) {
            if (expected == null || actual == null) {
                return "invalid record";
            }
            if (expected.getValue() != actual.getValue()) {
                return "invalid value";
            }
            return null;
        }
    }

``ModelVerifier`` を実装したクラスを作成したら、各 ``Tester`` クラスの ``output.verify()`` メソッドの第二引数に指定します。

..  code-block:: java

    @Test
    public void testExample() {
        JobFlowTester tester = new JobFlowTester(getClass());
        tester.input("shipment", Shipment.class)
            .prepare("shipment.xls#input");
        tester.output("hoge", Hoge.class)
            .verify("hoge.json", new ExampleVerifier());
        ...
    }

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.core.ModelVerifier`

テスト条件をJavaで拡張する
~~~~~~~~~~~~~~~~~~~~~~~~~~

`テスト条件をJavaで記述する`_ で説明した方法ではテスト条件をすべてJavaで記述しますが、Excelなどで記述したテスト条件をJavaで拡張することもできます。

テスト条件をJavaで拡張するには、 ``ModelTester`` [#]_ インターフェースを実装したクラスを作成します。
このインターフェースは先述の ``ModelVerifier`` の親インターフェースとして宣言されており、以下のインターフェースメソッドが定義されています。

``Object verify(T expected, T actual)``
    突き合わせた2つのオブジェクトを比較し、比較に失敗した場合にはその旨のメッセージを返す。成功した場合には ``null`` を返す。

``ModelTester`` インターフェースを利用したテストでは、次のように期待データと結果の比較を行います。

#. Excel等で記述したテスト条件で期待データと結果データの突き合わせと比較を行う
#. 上記で突き合わせに成功したら、 ``ModelTester.verify(<期待データ>, <結果データ>)`` で比較を行う
#. 両者の比較のうちいずれかに失敗したらテストは失敗となる

以下は ``ModelTester`` インターフェースの実装例です。

..  code-block:: java

    class ExampleTester implements ModelTester<Hoge> {

        @Override
        public Object verify(Hoge expected, Hoge actual) {
            if (expected == null || actual == null) {
                return "invalid record";
            }
            if (expected.getValue() != actual.getValue()) {
                return "invalid value";
            }
            return null;
        }
    }

``ModelTester`` を実装したクラスを作成したら、各 ``Tester`` クラスの ``output.verify()`` メソッドの第三引数にそのインスタンスを指定します [#]_ 。

..  code-block:: java

    @Test
    public void testExample() {
        JobFlowTester tester = new JobFlowTester(getClass());
        tester.input("shipment", Shipment.class)
            .prepare("shipment.xls#input");
        tester.output("hoge", Hoge.class)
            .verify("hoge.json", "hoge.xls#rule", new ExampleTester());
        ...
    }

..  hint::
    ``ModelTester`` のインスタンスを指定する代わりに、比較ロジックを記述したラムダ式を指定することもできます。

テスト条件の拡張は、主にExcelなどで表現しきれない比較を行いたい場合に利用できます。
比較方法をすべてJavaで記述する場合には `テスト条件をJavaで記述する`_ の方法を参照してください。

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.core.ModelTester`

..  [#] 第三引数を指定できるのは、テスト条件をパスで指定した場合のみです。
        ``ModelVerifier`` を利用する場合には指定できません。

.. _testing-userguide-run-config:

テスト実行時の設定
==================

ここではテストドライバーでテスト実行時の環境や動作を設定するための機能を説明します。

コンテキストAPIを利用するデータフローのテスト
---------------------------------------------

テスト対象のデータフローでコンテキストAPIを利用している場合、コンテキストAPIが参照するバッチの起動引数をテスト側で指定します。
この設定には、 各 ``Tester`` クラスの ``setBatchArg`` というメソッドから設定します。

..  code-block:: java

    @Test
    public void testExample() {
        BatchTester tester = new BatchTester(getClass());
        tester.setBatchArg("message", "Hello, world!");
        ...
    }

上記のように、第一引数には変数名、第二引数には変数の値を指定します。

なお、データフローのテストでは `コンテキストAPIを利用する演算子のテスト`_ で必要な ``reload`` の指定は不要です。

.. _testing-runtime-plugin-configuration:

実行時プラグインを利用するデータフローのテスト
----------------------------------------------

テスト対象の演算子で実行時プラグイン [#]_ を利用する場合、「実行時プラグイン設定ファイル」が必要になります。
データフローのテストの際には、利用している開発環境にインストールされた設定ファイル [#]_ を利用して処理を実行します。

その他、各 ``Tester`` クラスの ``configure`` メソッドを利用して個々のプラグインの設定を行うことも可能です。

..  code-block:: java

    @Test
    public void testExample() {
        BatchTester tester = new BatchTester(getClass());
        tester.configure(
            "com.asakusafw.runtime.core.Report.Delegate", "com.example.CustomReportDelegate"
        );
        ...
    }

上記のように、第一引数にはプロパティ名、第二引数にはプロパティの値を指定します。

なお、データフローのテストでは `実行時プラグインを利用する演算子のテスト`_ で必要な ``reload`` の指定は不要です。

..  attention::
    実行時プラグインはの設定は、Hadoop起動時の "-D" オプションで指定するプロパティをそのまま利用しています。
    そのため、 ``configure`` メソッドでHadoopのプロパティを利用することも可能ですが、通常の場合は利用しないでください。

..  [#] :doc:`../administration/deployment-runtime-plugins` を参照
..  [#] :doc:`../application/gradle-plugin` の手順に従って作成したプロジェクトでは :file:`$ASAKUSA_HOME/core/conf/asakusa-resources.xml` が配置されるため、デフォルトの状態ではこのファイルが利用されます。
        デフォルトの状態では演算子のテストで使用される実行時プラグイン設定ファイルと異なるファイルが利用されることに注意してください。

テストドライバーの各実行ステップをスキップする
----------------------------------------------

テストドライバーは、各ステップをスキップするためのメソッドが提供されています。
これらのメソッドを使用することで、以下のようなことが可能になります。

* 入力データ設定前にクリーニング、および入力データの投入をスキップして既存データに対するテストを行う
* 出力データの検証をスキップしてテストドライバーAPIの外側で独自のロジックによる検証を行う。

スキップを行う場合、 ``Tester`` クラスが提供する以下のメソッドを利用します。

``void skipValidateCondition(boolean skip)``
    テスト条件の検証をスキップするかを設定する。

``void skipCleanInput(boolean skip)``
    入力データのクリーニング(truncate)をスキップするかを設定する。

``void skipCleanOutput(boolean skip)``
    出力データのクリーニング(truncate)をスキップするかを設定する。

``void skipPrepareInput(boolean skip)``
    入力データのセットアップ(prepare)をスキップするかを設定する。

``void skipPrepareOutput(boolean skip)``
    出力データのセットアップ(prepare)をスキップするかを設定する。

``void skipRunJobFlow(boolean skip)``
    ジョブフローの実行をスキップするかを設定する。

``void skipVerify(boolean skip)``
    テスト結果の検証をスキップするかを設定する。

.. _testing-userguide-debug-analysis:

その他のオプション
------------------

その他、各 ``Tester`` クラスで利用可能なテストの動作を設定するメソッドは以下の通りです。

``setExtraCompilerOption(String name, String value)``
    テストドライバー実行時にアプリケーションをコンパイルする際のコンパイラオプションを設定する。

テストのデバッグと実行結果の分析
================================

ここではテストドライバーを使ったテストのデバッグや実行結果の分析に利用できる補助機能について説明します。

データフローの出力結果を保存する
--------------------------------

テスト実行時のデータフローの出力結果をファイルに保存するには、各 ``Tester`` クラスの ``output()`` に続いて ``dumpActual("<出力先>")`` を指定します。

出力先には、ファイルパスや ``File`` [#]_ オブジェクトを指定できます。
ファイルパスで相対パスを指定した場合、テストを実行したワーキングディレクトリからの相対パス上に結果が出力されます。

出力先に指定したファイル名の拡張子に応じた形式で出力が行われます。
標準ではExcelシートを出力する ``.xls`` または ``.xlsx`` を指定できます。

..  code-block:: java

    Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
        .dumpActual("build/dump/actual.xls")
        .verify("shipment.xls#output", "shipment.xls#rule");

また、Direct I/Oが取り扱うことができるフォーマットファイルで出力することもできます。
この場合、`Direct I/Oファイルをテストドライバーで使用する`_ と同様に ``DataFormat`` の実装クラスと ``File`` オブジェクトを指定します。

..  code-block:: java

    Out<ErrorRecord> errorRecord = tester.output("errorRecord", ErrorRecord.class)
        .dumpActual(ErrorRecordCsvFormat.class, new File("build/dump/error-record.csv")
        .verify("error.xls#output", "error.xls#rule");

この操作は上記例のように ``verify()`` と組み合わせて利用することができます。

..  attention::
    EclipseなどのIDEを利用している場合、ファイルが出力された後にワークスペースの表示更新やリフレッシュなどを行うまで、出力されたファイルが見えない場合があります。

..  [#] ``java.io.File``

テスト実行の比較結果を保存する
------------------------------

テストドライバーに設定した期待データとテスト実行結果との比較結果をファイルに保存するには、対象の出力に対して ``dumpDifference(<出力先>)`` を指定します。

..  code-block:: java

    Out<Shipment> shipmentOut = tester.output("shipment", Shipment.class)
        .verify("shipment.xls#output", "shipment.xls#rule")
        .dumpDifference("build/dump/difference.html");

`データフローの出力結果を保存する`_ と同様に、出力先にはファイルパスや ``File`` オブジェクトを指定できます。
ファイルパスで相対パスを指定した場合、テストを実行したワーキングディレクトリからの相対パス上に結果が出力されます。

また、出力先に指定したファイル名の拡張子に応じた形式で出力が行われます。
標準ではHTMLファイルを出力する ``.html`` を指定できます。

この操作は、 ``verify()`` と組み合わせて指定してください。
``verify()`` の指定がない場合、比較結果の保存は行われません。
また、比較結果に差異がない場合には比較結果は保存されません。

演算子のトレースログを出力する
------------------------------

テスト対象のデータフローに含まれる演算子について、入力されたデータと出力されたデータを調べるには、テストドライバーのトレース機能を利用すると便利です。
トレース機能を利用すると、指定した演算子に入力されたデータや出力されたデータを :ref:`dsl-report-api` 経由で表示できます。

トレース機能はユーザー演算子に指定することができます。コア演算子にはトレースを指定することはできません。

入力データのトレース
~~~~~~~~~~~~~~~~~~~~

演算子に入力されたデータを調べる場合、各 ``Tester`` クラスの ``addInputTrace`` メソッドを利用して対象の演算子と入力ポートを指定します。
下記の例は、演算子クラス ``YourOperator`` に作成した演算子メソッド ``operatorName`` の入力ポート [#]_ ``inputName`` に入力される全てのデータについてトレースの設定を行います。

..  code-block:: java

    @Test
    public void testExample() {
        JobFlowTester tester = new JobFlowTester(getClass());
        tester.addInputTrace(YourOperator.class, "operatorName", "inputName");
        ...
    }

..  [#] 演算子ファクトリクラスに含まれる演算子ファクトリメソッドの引数名が入力ポート名に該当します。
        詳しくは :doc:`../dsl/user-guide` - :ref:`dsl-userguide-operator-factory` を参照してください。

出力データのトレース
~~~~~~~~~~~~~~~~~~~~

演算子から出力されたデータを調べる場合、各 ``Tester`` クラスの ``addOutputTrace`` メソッドを利用して対象の演算子と出力ポートを指定します。
下記の例は、演算子クラス ``YourOperator`` に作成した演算子メソッド ``operatorName`` の出力ポート [#]_ ``outputName`` から出力する全てのデータについてトレースの設定を行います。

..  code-block:: java

    @Test
    public void testExample() {
        JobFlowTester tester = new JobFlowTester(getClass());
        tester.addOutputTrace(YourOperator.class, "operatorName", "outputName");
        ...
    }

..  [#] 演算子ファクトリクラスに含まれる演算子オブジェクトクラスのフィールド名が出力ポート名に該当します。
        詳しくは :doc:`../dsl/user-guide` - :ref:`dsl-userguide-operator-factory` を参照してください。

トレース情報の出力
~~~~~~~~~~~~~~~~~~

上記の設定を行った状態でテストを実行すると、指定した演算子の入力や出力が行われるたびに、文字列 ``TRACE-`` を含むメッセージを :ref:`dsl-report-api` 経由で出力します [#]_ 。
ここには、トレースを設定した対象の情報や、実際に入出力が行われたデータの内容が含まれています。

..  attention::
    トレース機能を有効にすると、テストの実行に非常に時間がかかるようになる場合があります。

..  note::
    トレースの出力方式は将来変更される可能性があります。

..  [#] このとき、 ``Report.info()`` を利用してメッセージを出力しています。
        メッセージが正しく表示されない場合には、Report APIの設定を確認してください。

テストドライバー実行環境
========================

テストドライバーを使ったテストを実行する上で必要となる環境について説明します。

Asakusa Frameworkのインストール
-------------------------------

テストドライバーを実行する環境には開発環境用のAsakusa Frameworkをインストールしておく必要があります。

開発環境用のAsakusa Frameworkをインストールする手順については、以下のドキュメントなどを参照してください。

* :doc:`../introduction/start-guide` - :ref:`introduction-start-guide-install-asakusafw`

Windows用の実行ライブラリ
-------------------------

Windows上でテストドライバーを利用する場合、環境にVisual C++ 2010 ランタイム ライブラリがインストールされている必要があります。

環境にこのライブラリがインストールされていない場合、以下のサイトなどからライブラリを入手し、環境にインストールしてください。

*  `Microsoft Visual C++ 2010 再頒布可能パッケージ (x64) <https://www.microsoft.com/ja-jp/download/details.aspx?id=14632>`_

..  note::
    Visual C++ 2010 ランタイム ライブラリがインストールされていない環境上でテストを実行すると、
    以下のようなエラーメッセージが表示されテストの実行が失敗します。

    ..  code-block:: none

        java.lang.IllegalStateException: ExitCodeException exitCode=-1073741515:
        ...
        Caused by:
                ExitCodeException exitCode=-1073741515:

..  tip::
    Visual C++ 2010 ランタイム ライブラリは様々なソフトウェアに含まれるため、
    既にインストール済みになっている場合も多くあります。

.. _testing-userguide-integration-test:

インテグレーションテスト
========================

ここではバッチアプリケーションのインテグレーションテストを行ういくつかの方法と、テストツールの利用方法などについて説明します。

テスト方法とツール
------------------

バッチアプリケーションのインテグレーションテストを行うには、以下のような方法があります。

#. :doc:`YAESS <../yaess/index>` を利用してアプリケーションを実行する
#. :doc:`Asakusa CLI <../cli/index>` を利用してアプリケーションを実行する
#. `バッチテストランナー`_ を利用してアプリケーションを実行する
#. `テストツールタスク`_ を利用してアプリケーションを実行する

YAESS
  YAESSを利用する方法では、運用環境と同様の手順でバッチアプリケーションを実行するため、運用環境に近い確実なテストが行えます。

  その反面、各実行環境に応じた適切な設定を管理する必要があったり、標準の設定では運用環境を前提とした詳細なログが出力されたりと、開発環境上でちょっとした動作確認を行うにはやや煩雑です。

Asakusa CLI
  Asakusa CLI ( :program:`asakusa run` ) を利用する方法は、開発環境や運用環境で簡易的にバッチアプリケーションの動作確認を行う場合に適しています。

  アプリケーション情報の表示、およびDSL情報の可視化機能と統合したコマンドラインインターフェース、シンプルな設定、簡易的なログ出力などにより、簡単にすばやくバッチアプリケーションを実行し、その結果を確認、分析することができます。ただしYAESSのような実行時の細かい設定を管理することはできません。

バッチテストランナー
  バッチテストランナーは、テストドライバーの内部機構を利用して簡易的にバッチアプリケーションを実行するAPIです。コマンドラインインターフェースとしても利用することができます。
  テストドライバーと同様に、ローカルコンピューター上のAsakusa Framework実行環境を利用してバッチを実行します。

  複雑な自動テストを構築するための各種インターフェースとして利用するとよいでしょう。
  YAESSのような細かい実行設定を行うことはできないので、テスト実行以外の用途では利用すべきではありません。

テストツールタスク
  テストツールタスクはテストドライバーやバッチテストランナーが持つ機能を組み合わせてGradleのタスクとして実行できるようにするものです。
  YAESSやバッチテストランナーを使ってアプリケーションを実行しつつ、データ配置やデータの検証はテストドライバーの機構を利用する、という場合に利用することができます。

  テストツールタスクはインテグレーションテストの自動化を行う場合や、自動テストと手動テストを組み合わせるような場合などで利用することを想定しています。

以下はツールごとにおける自動化部分の比較です。

..  list-table:: ツールごとのインテグレーションテスト自動化部分の比較
    :widths: 1 1 1 1
    :header-rows: 1

    * - 項目
      - テストドライバー
      - バッチテストランナー
      - テストツールタスク
    * - アプリケーションのビルド
      - ○
      - ×
      - ×
    * - アプリケーションのデプロイ
      - ○
      - ×
      - ×
    * - 入力データの配置
      - ○
      - ×
      - ○
    * - アプリケーションの実行
      - ○
      - ○
      - ○
    * - 実行結果の確認
      - ○
      - ×
      - ○

.. _testing-userguide-batch-test-runner:

バッチテストランナー
--------------------

バッチテストランナーはテストドライバーが持つ機能のうち、アプリケーションの実行のみを単独で行えるようにしたものです。
テストドライバーが自動的に行っていたいくつかの部分について、手動で細やかな設定を行えるようになります。

バッチテストランナーを利用してアプリケーションを実行するには、バッチテストランナーのプログラミングインターフェースや、コマンドラインインターフェースを利用します。
詳しくは以降を参照してください。

..  hint::
    バッチテストランナーが自動的に行わない部分の手順については、 :ref:`startguide-running-example` などを参照してください。

プログラミングインターフェース
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Javaのプログラムからバッチテストランナーを実行するには、 ``com.asakusafw.testdriver.tools.runner.BatchTestRunner`` [#]_ クラスを利用します。
詳しい利用方法は、Javadocを参照してください。

以下は :ref:`Asakusa Framework スタートガイド <startguide-running-example>` で紹介しているサンプルアプリケーションを実行する例です。

..  code-block:: java

    int result = new BatchTestRunner("example.summarizeSales")
        .withArgument("date", "2011-04-01")
        .execute();

    if (result != 0) {
        // エラー処理 ...
    }

..  [#] :asakusafw-javadoc:`com.asakusafw.testdriver.tools.runner.BatchTestRunner`

コマンドラインインターフェース
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コマンドラインからバッチテストランナーを実行するには、テストドライバーのクラスライブラリ群をクラスパスに登録した状態で ``com.asakusafw.testdriver.tools.runner.BatchTestRunner`` クラスを実行します。

指定できるオプションは次の通りです。

..  program:: com.asakusafw.testdriver.tools.runner.BatchTestRunner

..  option:: -b,--batch <batch_id>

    実行するバッチのバッチIDを指定します。

..  option:: -A,--argument <name=value>

    実行するバッチのバッチ引数を指定します。

..  option:: -D,--property <name=value>

    :ref:`testing-runtime-plugin-configuration` を行います。

例えば :ref:`Asakusa Framework スタートガイド <startguide-running-example>` で紹介しているサンプルアプリケーションを実行する場合のオプション指定は以下のようになります。

..  code-block:: sh

    -b example.summarizeSales -A date=2011-04-01

コマンドラインインターフェースは、バッチアプリケーションが正常終了した際に終了コード ``0`` を返し、正常終了しなかった場合に非 ``0`` を返します。

.. _testing-userguide-testtool-task:

テストツールタスク
------------------

テストツールタスクはテストドライバーやバッチテストランナーが持つ機能を組み合わせてGradleのタスクとして実行できるようにするものです。
バッチの実行にはYAESSとバッチテストランナーのどちらかを選択します。

以下にテストツールタスクを使って作成したGradleタスクの例を示します。

..  code-block:: groovy

    task batchTestSummarize(type: com.asakusafw.gradle.tasks.TestToolTask) {
        clean description: 'com.example.batch.SummarizeBatch'
        prepare importer: 'com.example.jobflow.StoreInfoFromCsv',
            data: '/com/example/jobflow/masters.xls#store_info'
        prepare importer: 'com.example.jobflow.ItemInfoFromCsv',
            data: '/com/example/jobflow/masters.xls#item_info'
        prepare importer: 'com.example.jobflow.SalesDetailFromCsv',
            data: '/com/example/jobflow/summarize.xls#sales_detail'
        run batch: 'example.summarizeSales'
        verify exporter: 'com.example.jobflow.CategorySummaryToCsv',
            data: '/com/example/jobflow/summarize.xls#result',
            rule: '/com/example/jobflow/summarize.xls#result_rule'
    }

..  seealso::
    ``TestToolTask`` や Gradleの利用方法については :doc:`../application/gradle-plugin` を参照してください。
