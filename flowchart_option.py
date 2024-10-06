import json
from pydantic import BaseModel, Field, field_validator


class Node(BaseModel):
    """
    フローチャートのノードクラス

    属性:
        id (str): ノードのID
        name (str): ノードの名前
        type (str): ノードのタイプ
        function (str): ノードの機能
        argument (dict): ノードの引数
        description (str): ノードの説明
    """

    id: int = Field(default=0, title="ID of the node")
    name: str | None = Field(
        default=None, title="Name of the node"
    )
    type: str | None = Field(
        default=None, title="Type of the node"
    )
    function: str | float | None = Field(
        default=None, title="Function of the node"
    )
    argument: str | float | dict | None = Field(
        default=None, title="Argument of the node"
    )
    description: str | float | None = Field(
        default=None, title="Description of the node"
    )

    @field_validator("argument", mode="before")
    def convert_argument_to_dict(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for argument")
        elif isinstance(value, float):
            return None

        return value


class Edge(BaseModel):
    """
    フローチャートのエッジクラス

    属性:
        id (str): エッジのID
        source (str): エッジのソース
        target (str): エッジのターゲット
        condition (bool): エッジの条件
        description (str): エッジの説明
    """

    id: int = Field(default=0, title="ID of the edge")
    source: str | None = Field(default=None, title="Source of the edge")
    target: str | None = Field(default=None, title="Target of the edge")
    condition: str | float | bool | None = Field(
        default=None, title="Condition of the edge"
    )
    description: str | float | None = Field(
        default=None, title="Description of the edge"
    )

    @field_validator("condition", mode="before")
    def convert_condition_to_bool(cls, value):
        if isinstance(value, str):
            if value.lower() in ["true", "false"]:
                return value.lower() == "true"
            else:
                raise ValueError(
                    "Invalid string for condition, must be 'true' or 'false'")
        elif isinstance(value, float):
            return None

        return value


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
    current_node: Node | None = Field(
        default=None, title="Current node in the flowchart"
    )
    return_value: dict | None = Field(
        None, title="Return value of the node"
    )
    variables: dict = Field(
        default_factory=dict, title="Variables in the flowchart"
    )


class NodeResponse(BaseModel):
    """
    ノードのレスポンスクラス

    args:
        result (any): ノードの戻り値
        variables (dict): ノードの変数
        condition (bool): ノードの条件
        message (str): ノードから
    """

    result: dict | None = Field(
        default=None, title="Return value of the node"
    )
    condition: bool | None = Field(
        default=None, title="Condition of the node"
    )
    message: str | None = Field(
        default=None, title="Message from the node"
    )
