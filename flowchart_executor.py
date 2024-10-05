import json
import pandas as pd
from flowchart_option import Flowchart
from flowchart_option import Node
from flowchart_option import Edge


class FlowchartExecutor:
    def __init__(self):
        """
        FlowchartExecutorのコンストラクタ

        args:
            flowchart (dict): フローチャートの情報を格納した辞書


        """
        self.flowchart = None
        self.tools = {}
        self.node_map = {}  # ノード名をキーとするマップを追加

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
            self.flowchart.return_value = self.node_executor(
                self.flowchart.current_node
            )
            print(
                f"ノード '{self.flowchart.current_node.name}' の実行結果: {
                    self.flowchart.return_value}"
            )

            if not self.edge_executor(
                self.flowchart.current_node, self.flowchart.return_value
            ):
                break
            if self.flowchart.current_node.name == end_name:
                break

        # フローチャートの最終結果を返す
        return self.flowchart.return_value

    def find_node(self, node_name: str | None = None) -> Node | None:
        """
        ノードを検索する

        args:
            node_name (str): ノードの名前
        """
        return self.node_map.get(node_name)

    def node_executor(self, node: Node) -> dict | None:
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
                args = node.argument or {}
                if node.function == 'check_age':
                    args['age'] = self.flowchart.variables.get('age', 0)
                result = tool(**args)
                return_value = (
                    result if isinstance(result, dict) else {"result": result}
                )
                if 'age' in result:
                    self.flowchart.variables['age'] = result['age']
                return return_value
        return {"result": None}

    def edge_executor(self, node: Node, return_value: dict | None) -> bool:
        """
        エッジを実行する

        args:
            node (Node): ノード

        """
        # エッジを検索
        for edge in self.flowchart.edges:
            # エッジのソースがノードの名前と一致する場合
            if edge.source == node.name:
                if ((edge.condition is None)
                    or (
                        isinstance(return_value, dict)
                        and (return_value.get('condition') == edge.condition)
                )):
                    self.flowchart.current_node = self.find_node(edge.target)
                    return True
        return False

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
    sys.path.append(current_dir)

    tools_module = importlib.import_module('sample_tools')

    executor = FlowchartExecutor()

    executor.tools = {
        "greet": getattr(tools_module, 'greet'),
        "random_age": getattr(tools_module, 'random_age'),
        "check_age": getattr(tools_module, 'check_age'),
        "adult_message": getattr(tools_module, 'adult_message'),
        "child_message": getattr(tools_module, 'child_message')
    }

    # json_file_path = os.path.join(current_dir, 'sample.json')
    # executor.load_json(json_file_path)
    excel_file_path = os.path.join(current_dir, 'sample.xlsx')
    executor.load_excel(excel_file_path)

    if executor.flowchart is None:
        print("フローチャートのロードに失敗しました。")
    else:
        print("フローチャートの実行結果:")
        result = executor.execute()
        print("最終結果:", result)
