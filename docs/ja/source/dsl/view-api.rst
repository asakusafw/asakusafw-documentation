=========
ビューAPI
=========

ビューAPIはAsakusa DSLの拡張機能で、データフロー上の任意の中間出力を、演算子から柔軟に参照するためのインターフェースを提供します。ビューは主にバッチ全体の定数表を効率よく扱うためのしくみで、以下のような定数データを外部データソースから取り込んで演算子メソッドから利用できます。

以下は「消費税率」などの税率テーブルをデータベースなどに保持し、演算子内から参照するサンプルコード片です。

..  code-block:: java
    :emphasize-lines: 11

    private static final StringOption KEY_CTAX = new StringOption("消費税");

    /**
     * 消費税を計算する。
     * @param detail 販売明細
     * @param taxTable 税率テーブル
     */
    @Update
    public void updateTax(
            SalesDetail detail,
            @Key(group = "name") GroupView<TaxEntry> taxTable) {

        // 税率テーブルから「消費税」に関する情報を取得する
        TaxEntry tax = taxTable.find(KEY_CTAX).get(0);

        // 総額から本体価格を算出する
        BigDecimal totalPrice = BigDecimal.valueOf(detail.getSellingPrice());
        BigDecimal priceWithoutTax = totalPrice.divide(BigDecimal.ONE.add(tax.getRate()));

        // ...
    }

また、バッチ内で作成した中間データ（集計結果など）を上記と同様に定数表として参照したり、柔軟なテーブル化の機能を利用して複雑な条件を伴う結合処理（例えばデータ範囲を条件とする結合）などを、効率よく実現したりすることが可能です。

..  attention::
    Asakusa on MapReduceではビューAPIを利用できません。

概要
====

ビューAPIを利用することで、Asakusa DSLで以下のようなデータアクセスが可能になります。

* Direct I/OやWindGateなどの外部入力データに、任意の演算子から読み取り専用でアクセスする。
* 任意の演算子の途中結果に、任意の演算子から読み取り専用でアクセスする。
* 結合演算子を利用した結合系処理とは異なり、付き合わせを行うことなく指定したデータの全体に参照する。

ビューAPIを使用するには、ビューAPIが提供するインターフェースを演算子メソッドの引数（ビュー引数）として指定します。
ビュー引数を経由して、ビューに指定した入力に対するすべてのレコードにアクセスすることができます。

ビューAPIには、参照するデータ全体を順次参照するための ``View`` [#]_ インターフェースと、特定のキーを持つグループを選択して参照するための ``GroupView`` [#]_ インターフェースがあります。

``GroupView`` インターフェースは、``View`` インターフェースの機能に加えて、以下の機能を提供します。

* パーティショニング用のキーを指定し、キーに対するグループ単位でレコードにアクセスする。
* グループ化するデータセットに対して任意の整列順序を指定する。

グループ化や整列が処理効率に影響するような処理を記述する場合は、``GroupView`` インターフェースの利用を推奨します。

..  [#] :asakusafw-javadoc:`com.asakusafw.runtime.core.View`
..  [#] :asakusafw-javadoc:`com.asakusafw.runtime.core.GroupView`

ビューAPIの利用方法
===================

ビューAPIを利用したバッチアプリケーションを作成するには、まずOprator DSL上でビューAPIインターフェースを利用した演算子メソッドを作成します。Flow DSL上ではその演算子に対して、従来と同様の方法でデータフローの入力を指定します。

演算子メソッドの定義
--------------------

ビューAPIを利用する演算子メソッドを作成するには、メソッドの引数を定義する際に **入力データを受け取る引数の直後** に ``View<T>`` 、または ``GroupView<T>`` の引数を指定します。
型変数 ``T`` にはこのAPIを通してアクセスするデータモデルクラスの型を指定します。

以下は、更新演算子で ``View`` を利用する演算子メソッドの定義例です。

..  code-block:: java
    :emphasize-lines: 4

    @Update
    public void updateWithView(
            SalesDetail sales,
            View<Foo> view) {
        ...
    }

``GroupView`` を利用する場合には以下の例のように  ``GroupView<T>`` の直前に ``@Key`` 注釈 ( :ref:`dsl-key-annotation` )を指定して、グループ化キー ( ``group`` )を指定する必要があります。
また、 ``order`` を指定することで、グループ内の要素の順序を指定できます。

以下は、抽出演算子で ``GroupView`` を利用する演算子メソッドの定義例です。
``GroupView`` を定義する引数の位置に注目してください。

..  code-block:: java
    :emphasize-lines: 4

    @Extract
    public void extractWithGroupView(
            SalesDetail sales,
            @Key(group = "store_code", order = "id") GroupView<Foo> view,
            Result<SalesDetail> result,
            Result<ErrorRecord> error) {
        ...
    }

演算子メソッドの実装
--------------------

``View<T>`` は ``Iterable<T>`` インターフェースを継承しています。
そのため、``View<T>`` からレコードにアクセスするには拡張for文(for-each文)などを利用することができます。この方法でレコードにアクセスする場合、取り出されるレコードの整列順序は不定です。

..  code-block:: java
    :emphasize-lines: 6

    @Update
    public void updateWithView(
            SalesDetail sales,
            View<Foo> view) {

        for (Foo foo : view) {
            ...
        }
    }


``GroupView<T>`` では ``find`` メソッドを使用して、キー注釈で指定したグループに対応するレコードを ``List<T>`` として取得できます。このリストに含まれるレコードはキー注釈で指定した整列順序で整列されています。

..  code-block:: java
    :emphasize-lines: 8

    @Extract
    public void extractWithGroupView(
            SalesDetail sales,
            @Key(group = "store_code", order = "id") GroupView<Foo> view,
            Result<SalesDetail> result,
            Result<ErrorRecord> error) {

        List<Foo> fooList = view.find(sales.getStoreCodeOption());
        ...
    }

..  attention::
    ``GroupView<T>`` は ``View<T>`` のサブインターフェースであるため、 ``View<T>`` と同様の方法でもレコードにアクセスすることもできます。ただしこの方法ではキー注釈で指定した整列順序は不定です。

``find`` メソッドに指定する引数には、キー注釈で指定したグループに対応したデータ項目を入力のデータモデルクラスから指定します。このとき、引数に指定する値はデータモデルクラスの ``getXXXOption`` で取得できる ``ValueOption`` のサブクラスを指定する必要があります。

上記の例では、 ``GroupView<Foo> view`` にはキー注釈でDMDLのTEXT型として定義した ``store_code`` をグループとして指定しているので、 このビューの ``find`` メソッドに指定可能な引数は1つで、その型は ``StringOption`` になります。

..  attention::
    上記の例では ``find`` メソッドに ``sales.getStoreCodeOption()`` で返される ``StringOption`` 型を指定することができますが、 ``sales.getStoreCode()`` で返される ``Text`` 型や ``sales.getStoreCodeAsString()`` で返される ``String`` 型を指定することはできません。

..  attention::
    ``find`` メソッドに指定する引数の数は、必ずキー注釈で指定したグループの個数と同じ数を指定してください。引数の数が一致しない場合でもコンパイルエラーにはなりませんが、実行時には正しく動作しません。

演算子メソッド実装の制約
------------------------

* ビューAPIで取得するすべてのオブジェクトはメモリ上に保持されます。ビューAPIで取得するレコード数が膨大となる場合、メモリ不足で実行に失敗する可能性があります。
* ビューAPI経由で取得したデータモデルオブジェクトの内容は変更できません。変更した場合の実行結果は不定です。
* ビューAPI経由で取得したデータモデルオブジェクトの値を演算子の出力に指定することはできません。ただしデータモデルオブジェクトの値をコピーして、その値を出力に指定することは可能です。
* メソッド本体の実装が不要なユーザー演算子に対して、ビューAPIを使用することはできません。ただし例外として、マスタ選択( ``@MasterSelection`` )補助演算子を伴う演算子については、実装が不要な演算子に対してビューAPIを使用することができます。
* 畳み込み演算子( ``@Fold`` )では部分集約を有効にしている場合、ビュー引数を指定することはできません。

..  seealso::
    各演算子の詳細については、 :doc:`operators` を参照してください。

演算子メソッドの例
------------------

複数のビュー
~~~~~~~~~~~~

演算子では任意の個数のビューを利用することができます。

..  code-block:: java

    @MasterJoinUpdate
    public void masterJoinWithGroupView(
            @Key(group = "store_code") StoreInfo store,
            @Key(group = "store_code") SalesDetail sales,
            @Key(group = "store_code") GroupView<StoreInfo> viewStoreA,
            @Key(group = "store_code") GroupView<StoreInfo> viewStoreB,
            @Key(group = "store_code") GroupView<StoreInfo> viewStoreC
            ) {
        ...
    }

値引数を含む演算子
~~~~~~~~~~~~~~~~~~

値引数を利用する演算子メソッドでビューを利用する場合、引数の順序は以下のようになります

* 入力データを受け取る引数
* ビュー引数
* 出力データを格納する引数
* 値引数

..  code-block:: java

    @GroupSort
    public void groupSortWithView(
            @Key(group = "store_code", order = "amount DESC") List<SalesDetail> sales,
            View<ItemInfo> viewItem,
            Result<SalesDetail> result,
            int numberOfRank) {
        ...
    }

マスタ選択演算子の利用
~~~~~~~~~~~~~~~~~~~~~~

マスタ選択演算子でビューを利用するには、対応する演算子側にもビュー引数を定義する必要があります。

..  code-block:: java

    @MasterCheck(selection = "selectAvailableItem")
    public abstract boolean masterSelectionWithGroupView(
            @Key(group = "item_code") ItemInfo info,
            @Key(group = "item_code") SalesDetail sales,
            @Key(group = "item_code") GroupView<ItemInfo> viewItem);

    @MasterSelection
    public ItemInfo selectAvailableItem(
            List<ItemInfo> candidates,
            SalesDetail sales,
            GroupView<ItemInfo> viewItem) {
        ...
    }

``GroupView`` を利用する場合、グループ化の定義は対応する演算子側のキー注釈の定義が利用されます。マスタ選択演算子側にキー注釈を指定しても、その内容は無視されます。

グループ化キーの定義
~~~~~~~~~~~~~~~~~~~~

``GroupView`` で指定するグループ化キーは、結合のためのキーとは別の項目を指定することができます。

..  code-block:: java

    @CoGroup
    public void cogroupViewGroupView(
            @Key(group = "store_code") List<SalesDetail> salesA,
            @Key(group = "store_code") List<SalesDetail> salesB,
            @Key(group = "item_code") GroupView<ItemInfo> viewItem,
            Result<Foo> result) {
        ...
    }

フロー記述メソッドの実装
------------------------

Flow DSLでビューAPIを使用した演算子を利用するデータフローを記述するには、通常の演算子の入力を指定する方法と同じように、演算子に定義した入力に対してデータフローの接続を指定します。

..  code-block:: java

    @FlowPart
    public class WithViewFlowPart extends FlowDescription {

        final In<SalesDetail> salesDetail;
        final In<Foo> fooView;
        ...

        @Override
        protected void describe() {
            WithViewOperatorFactory operators = new WithViewOperatorFactory();
            UpdateWithView updateWithView = operators.updateWithView(salesDetail, fooView);
            ...
        }

    }

この例では ``updateWithView`` 演算子に2つの入力を渡しています。第1引数は通常の入力、第2引数はビューAPIを使用して定義した入力ですが、Flow DSLでは両者の入力は同じように取り扱うことができます。

テスト方法
==========

演算子メソッドのテスト
----------------------

演算子のテストでは、``DataLoader`` を利用して ``View<T>`` や ``GroupView<T>`` に対応するデータモデルオブジェクトを生成することができます。

詳しくは、:doc:`../testing/user-guide` - 演算子のテスト - :ref:`testing-userguide-viewapi` を参照してください。

データフローのテスト
--------------------

ビューAPIを使用する演算子を含むデータフローは、通常のデータフローと同様の方法でテストを記述することができます。

詳しくは :doc:`../testing/user-guide` - :ref:`testing-userguide-dataflow-testing` などを参照してください。
