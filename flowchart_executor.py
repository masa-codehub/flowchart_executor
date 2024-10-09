import json
import inspect
import pandas as pd
from .flowchart_option import Flowchart
from .flowchart_option import Node
from .flowchart_option import Edge
from .flowchart_option import NodeResponse


class FlowchartExecutor:
    def __init__(self):
        """
        FlowchartExecutorのコンストラクタ

        args:
            flowchart (dict): フローチャートの情報を格納した辞書


        """
        self.flowchart = None
        self.history = []
        self.tools = {}
        self.node_map = {}  # ノード名をキーとするマップを追加
        self.variables = {}

    def execute(self, start_name: str | None = None, end_name: str | None = None):
        """
        フローチャートを実行する

        Args:
            start_name (str | None): 開始ノードの名前。Noneの場合は最初のノードから開始
            end_name (str | None): 終了ノードの名前。Noneの場合は最後のノードまで実行

        Returns:
            None
        """

        # フローチャートが存在しない場合
        if self.flowchart is None:
            return None

        # 開始ノードを設定
        self.flowchart.current_node = (
            self.find_node(start_name) or self.flowchart.nodes[0]
        )

        # フローチャートの実行
        while self.flowchart.current_node is not None:
            # ノードを実行
            self.flowchart.return_value = self.node_executor(
                self.flowchart.current_node
            )

            # エッジを実行
            self.flowchart.current_node = self.edge_executor(
                self.flowchart.current_node, self.flowchart.return_value
            )

            # 終了条件のチェック
            if self.flowchart.current_node is None:
                break
            if end_name is not None:
                if self.flowchart.current_node.name == end_name:
                    break

        # フローチャートの最終結果を返す
        return self.flowchart.return_value

    def next(self):
        """
        現在のノードを実行し、次のノードに進む

        Returns:
        dict: 実行結果と次のノードの情報を含む辞書
        """

        # フローチャートが存在しない場合
        if (self.flowchart is None) or (self.flowchart.current_node is None):
            return None

        # フローチャートの実行
        while self.flowchart.current_node is not None:
            # ノードを実行
            self.flowchart.return_value = self.node_executor(
                self.flowchart.current_node
            )

            # エッジを実行
            self.flowchart.current_node = self.edge_executor(
                self.flowchart.current_node, self.flowchart.return_value
            )

            # 終了条件のチェック
            if self.flowchart.current_node is None:
                break
            if self.flowchart.current_node.type != "decision":
                break

        # フローチャートの最終結果を返す
        return self.flowchart.current_node

    def find_node(self, node_name: str | None = None) -> Node | None:
        """
        ノードを検索する

        args:
            node_name (str): ノードの名前
        """
        return self.node_map.get(node_name)

    def node_executor(self, node: Node) -> NodeResponse:
        """
        ノードを実行する

        args:
            node (Node): ノード
        """
        # ツールが登録されている場合
        if self.tools and node.function in self.tools:
            tool = self.tools[node.function]
            # ツールが呼び出し可能な場合
            if callable(tool):
                # ツールの引数を取得
                tool_params = inspect.signature(tool).parameters

                # ノードの引数を取得
                args = {
                    k: v for k, v in {**self.variables, **(node.argument or {})}.items()
                    if k in tool_params.keys()
                }

                # ツールを実行
                response = tool(**args)

                if response.result is not None:
                    self.variables.update(response.result)

                self.history.append({
                    "node": node.name,
                    "response": response.model_dump()
                })

        else:
            response = NodeResponse(message=f"ツール '{node.function}' が見つかりません。")
            self.history.append({
                "node": node.name,
                "response": response.model_dump()
            })

        return response

    def edge_executor(self, node: Node, return_value: NodeResponse | None) -> Node | None:
        """
        エッジを実行する

        args:
            node (Node): ノード

        """
        # エッジを検索
        for edge in self.flowchart.edges:
            # エッジのソースがノードの名前と一致する場合
            if edge.source == node.name:
                if ((edge.condition is None) or (return_value.condition == edge.condition)):
                    return self.find_node(edge.target)

        return None

    def load_excel(self, file_path: str | None = None):
        """
        フローチャートをロードする

        args:
            flowchart (dict): フローチャートの情報を格納した辞書

        """
        try:
            # 拡張子を取得する

            if file_path.endswith('.xlsx'):
                edges = pd.read_excel(file_path, sheet_name='edges')
                nodes = pd.read_excel(file_path, sheet_name='nodes')
            elif file_path.endswith('.csv'):
                edges = pd.read_csv(file_path, sheet_name='edges')
                nodes = pd.read_csv(file_path, sheet_name='nodes')
            else:
                raise ValueError("Unsupported file format. Use .xlsx or .csv")

            self.flowchart = Flowchart(
                nodes=[Node(**node) for node in nodes.to_dict('records')],
                edges=[Edge(**edge) for edge in edges.to_dict('records')]
            )
            self.node_map = {
                node.name: node for node in self.flowchart.nodes
            }

        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
        except pd.errors.EmptyDataError:
            print(f"ファイルが空です: {file_path}")
        except Exception as e:
            print(f"ファイルの読み込み中にエラーが発生しました: {e}")

    def load_json(self, file_path: str | None = None):
        """
        フローチャートをロードする

        args:
            flowchart (dict): フローチャートの情報を格納した辞書

        """
        try:
            with open(file_path, 'r') as f:
                flowchart_data = json.load(f)

            # ノードとエッジを直接作成
            nodes = [Node(**node) for node in flowchart_data.get('nodes', [])]
            edges = [Edge(**edge) for edge in flowchart_data.get('edges', [])]

            self.flowchart = Flowchart(nodes=nodes, edges=edges)

            # ノードマップを更新
            self.node_map = {node.name: node for node in self.flowchart.nodes}
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
        except json.JSONDecodeError:
            print(f"JSONの解析に失敗しました: {file_path}")
        except Exception as e:
            print(f"ファイルの読み込み中にエラーが発生しました: {e}")


if __name__ == '__main__':
    import importlib
    import os
    import sys

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(current_dir, '.sample')
    sys.path.append(sample_dir)

    tools_module = importlib.import_module('sample_tools')

    executor = FlowchartExecutor()

    executor.tools = {
        "greet": getattr(tools_module, 'greet'),
        "random_age": getattr(tools_module, 'random_age'),
        "check_age": getattr(tools_module, 'check_age'),
        "adult_message": getattr(tools_module, 'adult_message'),
        "child_message": getattr(tools_module, 'child_message')
    }

    # json_file_path = os.path.join(current_dir, './.sample/sample.json')
    # executor.load_json(json_file_path)
    excel_file_path = os.path.join(current_dir, './.sample/sample.xlsx')
    executor.load_excel(excel_file_path)

    if executor.flowchart is None:
        print("フローチャートのロードに失敗しました。")
    else:
        print("フローチャートの実行結果:")
        result = executor.execute()
        print("最終結果:")
        for route in executor.history:
            print(route)
