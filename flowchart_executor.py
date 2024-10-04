import json
import pandas as pd
from .flowchart_option import Flowchart
from .flowchart_option import Node


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

        if self.flowchart is None:
            return None

        # ノードの実行関数を登録
        self.flowchart.current_node = self.find_node(start_name)
        if self.flowchart.current_node is not None:
            #
            while self.flowchart.current_node is not None:
                self.node_executors(self.flowchart.current_node)
                self.edge_executors(self.flowchart.current_node)

                if self.flowchart.current_node.name == end_name:
                    break

        return None

    def find_node(self, node_name: str | None = None) -> Node | None:
        """
        ノードを検索する

        args:
            node_name (str): ノードの名前
        """
        return self.node_map.get(node_name)

    def node_executors(self, node: Node) -> bool:
        """
        ノードを実行する

        args:

        """
        # startノードが指定されている場合は、指定されたノードから実行を開始
        if self.tools:
            # ツールが登録されている場合は、ツールを実行
            if node.function in self.tools.keys():
                if self.tools[node.function] is not None:
                    # ツールの実行結果を変数に格納
                    self.flowchart.return_value = self.tools[node.function](
                        **node.argument,
                        **self.flowchart.variables,
                        **self.flowchart.return_value
                    )

                    return True
        return False

    def edge_executors(self, node: Node) -> bool:
        """
        エッジを実行する

        args:
            node (Node): ノード

        """
        # for edge in self.flowchart.edges:
        #     if edge.source == node.name:
        #         # エッジの条件が指定されていない場合は、次のノードを実行
        #         if edge.condition is None:
        #             self.flowchart.current_node = self.find_node(edge.target)
        #             return True
        #         else:
        #             # エッジの条件が指定されている場合は、条件を満たす場合のみ次のノードを実行
        #             if self.flowchart.return_value is not None:
        #                 if 'condition' in self.flowchart.return_value.keys():
        #                     if edge.condition == self.flowchart.return_value['condition']:
        #                         self.flowchart.current_node = self.find_node(
        #                             edge.target
        #                         )
        #                         return True

        for edge in self.flowchart.edges:
            if edge.source == node.name:
                if edge.condition is None or (
                    (self.flowchart.return_value is not None)
                    and (self.flowchart.return_value.get('condition') == edge.condition)
                ):
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

            self.flowchart = Flowchart(
                nodes=nodes, edges=edges
            )  # type: ignore
            self.node_map = {node.name: node for node in self.flowchart.nodes}

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
            # 信頼できるキーのみを抽出
            safe_data = {
                k: v for k, v in flowchart_data.items() if k in Flowchart.model_fields()
            }
            self.flowchart = Flowchart(**safe_data)
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
        except json.JSONDecodeError:
            print(f"JSONの解析に失敗しました: {file_path}")
        except Exception as e:
            print(f"ファイルの読み込み中にエラーが発生しました: {e}")
