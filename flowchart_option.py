from pydantic import BaseModel, Field


class Node(BaseModel):
    """
    フローチャートのノードクラス

    属性:
        id (str): ノードのID
        name (str): ノードの名前
        type (str): ノードのタイプ
        function (str): ノードの機能
        augument (dict): ノードの引数
        description (str): ノードの説明
    """

    id: int = Field(default=0, title="ID of the node")
    name: str | None = Field(None, title="Name of the node")
    type: str | None = Field(None, title="Type of the node")
    function: str | None = Field(None, title="Function of the node")
    argument: dict | None = Field(None, title="Augument of the node")
    description: str = Field(None, title="Description of the node")


class Edge(BaseModel):
    """
    フローチャートのエッジクラス

    属性:
        id (str): エッジのID
        source (str): エッジのソース
        target (int): エッジのターゲット
        condition (bool): エッジの条件
        description (str): エッジの説明
    """

    id: int = Field(default=0, title="ID of the edge")
    source: str | None = Field(None, title="Source of the edge")
    target: int | None = Field(None, title="Target of the edge")
    condition: bool | None = Field(None, title="Condition of the edge")
    description: str = Field(None, title="Description of the edge")


class Flowchart(BaseModel):
    """
    フローチャートクラス

    属性:
        nodes (list[Node]): フローチャート内のノードのリスト
        edges (list[Edge]): フローチャート内のエッジのリスト
        current_node (Node): フローチャート内の現在のノード
        return_value (dict): ノードの戻り値
        variables (dict): フローチャート内の変数
    """

    nodes: list[Node] = Field(
        default_factory=list, title="List of nodes in the flowchart"
    )
    edges: list[Edge] = Field(
        default_factory=list, title="List of edges in the flowchart"
    )
    current_node_name: Node | None = Field(
        default=None, title="Current node in the flowchart"
    )
    return_value: dict | None = Field(
        None, title="Return value of the node"
    )
    variables: dict = Field(
        default_factory=dict, title="Variables in the flowchart"
    )
