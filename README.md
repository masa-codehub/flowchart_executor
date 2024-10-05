この記事は生成AIを使用して記述されています。

## 開発の背景
関数呼び出すだけのコードを書くのが面倒。jsonとかExcelで記述して、実行出来たらちょっとは楽になるかなーくらいの気持ちで軽く書いてみました。

https://github.com/masa-codehub/flowchart_executor

## FlowchartExecutorの主な特徴

1. **柔軟なデータ入力**: エクセルファイルやJSONファイルからフローチャートの定義を読み込むことができます。

2. **ノードとエッジの概念**: フローチャートの各要素をノードとエッジとして定義し、それぞれに役割を持たせることができます。

3. **カスタム関数の使用**: 各ノードに対して、カスタム関数を割り当てることができます。

4. **変数の管理**: フローチャート内で使用する変数を簡単に管理できます。

5. **実行履歴の記録**: フローチャートの実行履歴を記録し、後から確認することができます。

## 使用方法

FlowchartExecutorの基本的な使用方法は以下の通りです：

1. フローチャートの定義をエクセルまたはJSONファイルで作成します。
2. FlowchartExecutorのインスタンスを作成します。
3. `load_excel()`または`load_json()`メソッドを使用して、フローチャートの定義を読み込みます。
4. `execute()`メソッドを呼び出して、フローチャートを実行します。

以下は、使用例のコードスニペットです：

```python
executor = FlowchartExecutor()
executor.load_excel('flowchart.xlsx')
result = executor.execute()
```

## ユースケース

FlowchartExecutorは、様々な場面で活用することができます。以下にいくつかの例を挙げてみましょう。

### 1. 顧客サポートチャットボット

顧客からの問い合わせに対する応答フローをフローチャートで定義し、FlowchartExecutorを使用して実装することができます。これにより、複雑な条件分岐を含む応答ロジックを簡単に管理できます。

### 2. 診断ツール

医療や機械の故障診断など、一連の質問と回答によって結論を導き出すようなシステムをFlowchartExecutorで実装できます。フローチャートの変更が即座にシステムに反映されるため、診断ロジックの更新が容易になります。

### 3. ゲームのストーリー分岐

テキストベースのアドベンチャーゲームなど、プレイヤーの選択によってストーリーが分岐するゲームのロジックをFlowchartExecutorで実装できます。ストーリーの追加や変更が簡単に行えるため、ゲーム開発の効率が向上します。

### 4. ビジネスルールエンジン

企業の業務ルールや意思決定プロセスをフローチャートで表現し、FlowchartExecutorを使って実装することができます。ビジネスアナリストがフローチャートを更新するだけで、システムの動作を変更できるため、開発者の負担を軽減できます。

## FlowchartExecutorの概要

FlowchartExecutorは、Pythonで実装されたフローチャート実行ツールです。エクセルやJSONファイルで定義されたフローチャートを読み込み、実行することができます。

## 主要なクラスとその役割

FlowchartExecutorは、以下の主要なクラスで構成されています：

1. **Node**: フローチャートのノードを表現
2. **Edge**: フローチャートのエッジ（ノード間の接続）を表現
3. **Flowchart**: フローチャート全体を管理
4. **FlowchartExecutor**: フローチャートの実行を制御

## コードの詳細解説

### Node クラス

```python
class Node(BaseModel):
    id: int = Field(default=0, title="ID of the node")
    name: str | None = Field(default=None, title="Name of the node")
    type: str | None = Field(default=None, title="Type of the node")
    function: str | float | None = Field(default=None, title="Function of the node")
    argument: str | float | dict | None = Field(default=None, title="Argument of the node")
    description: str | float | None = Field(default=None, title="Description of the node")
```

このクラスは、フローチャートの各ノードを表現します。`id`、`name`、`type`、`function`、`argument`、`description`の属性を持ち、ノードの特性を定義します[1]。

### Edge クラス

```python
class Edge(BaseModel):
    id: int = Field(default=0, title="ID of the edge")
    source: str | None = Field(default=None, title="Source of the edge")
    target: str | None = Field(default=None, title="Target of the edge")
    condition: str | float | bool | None = Field(default=None, title="Condition of the edge")
    description: str | float | None = Field(default=None, title="Description of the edge")
```

Edgeクラスは、ノード間の接続を表現します。`source`と`target`でつながるノードを指定し、`condition`で分岐条件を設定できます[1]。

### FlowchartExecutor クラス

FlowchartExecutorクラスは、フローチャートの実行を制御する中心的なクラスです。主要なメソッドを見ていきましょう。

#### execute メソッド

```python
def execute(self, start_name: str | None = None, end_name: str | None = None):
    # ... (省略)
    while self.flowchart.current_node is not None:
        print(self.flowchart.current_node.name)
        self.flowchart.return_value = self.node_executor(self.flowchart.current_node)
        self.flowchart.current_node = self.edge_executor(
            self.flowchart.current_node, self.flowchart.return_value
        )
        # ... (省略)
```

このメソッドは、フローチャート全体の実行を制御します。各ノードを順番に実行し、エッジに基づいて次のノードに移動します[2]。

#### node_executor メソッド

```python
def node_executor(self, node: Node) -> dict | None:
    if self.tools and node.function in self.tools:
        tool = self.tools[node.function]
        if callable(tool):
            # ... (省略)
            response = tool(**args)
            if response.variables is not None:
                self.flowchart.variables.update(response.variables)
            # ... (省略)
    return response
```

このメソッドは、各ノードに割り当てられた関数を実行します。`self.tools`に登録された関数を呼び出し、その結果を処理します[2]。

#### load_excel メソッド

```python
def load_excel(self, file_path: str | None = None):
    # ... (省略)
    edges = pd.read_excel(file_path, sheet_name='edges')
    nodes = pd.read_excel(file_path, sheet_name='nodes')
    self.flowchart = Flowchart(
        nodes=[Node(**node) for node in nodes.to_dict('records')],
        edges=[Edge(**edge) for edge in edges.to_dict('records')]
    )
    # ... (省略)
```

このメソッドは、Excelファイルからフローチャートの定義を読み込みます。`nodes`シートと`edges`シートから情報を取得し、Flowchartオブジェクトを生成します[2]。

## ユースケース: 年齢チェックフローチャート

提供されたサンプルコードを使用して、簡単な年齢チェックフローチャートを実装してみましょう。

```python
import random
from flowchart_option import NodeResponse

def greet(name):
    return NodeResponse(message=f"Hello, {name}!")

def random_age():
    age = random.randint(1, 30)
    return NodeResponse(variables={"age": age}, message=f"Your age is {age}.")

def check_age(age):
    return NodeResponse(condition=age >= 18, message="You are an adult. Exiting.")

def adult_message():
    return NodeResponse(message="You are an adult. Exiting.")

def child_message():
    return NodeResponse(message="You are a child. Trying again.")
```

このコードは、年齢をランダムに生成し、18歳以上かどうかをチェックするフローチャートを定義しています[4]。

## まとめ

FlowchartExecutorを使用することで、複雑なロジックをフローチャートとして視覚化し、それを直接実行可能なコードに変換することができます。これにより、以下のような利点があります：

1. **ロジックの可視化**: フローチャートを使用することで、複雑なプロセスを視覚的に理解しやすくなります。
2. **迅速な開発**: フローチャートの変更がすぐにコードに反映されるため、開発サイクルが短縮されます。
3. **非エンジニアとの協業**: フローチャートは非技術者にも理解しやすいため、ビジネス側との協業が容易になります。

あとはChatGPTのAPIとか使ってフローチャート書かせたら自分で考えて色々仕事してくれるようになってくれないかなぁと妄想中。
