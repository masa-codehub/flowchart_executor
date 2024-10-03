from pydantic import BaseModel, Field


class Node(BaseModel):
    """
    Node class for the flowchart

    Attributes:
        id (str): ID of the node
        name (str): Name of the node
        function (str): Function of the node
        description (str): Description of the node
    """

    id: int = Field(default=0, title="ID of the node")
    name: str | None = Field(None, title="Name of the node")
    type: str | None = Field(None, title="Type of the node")
    function: str | None = Field(None, title="Function of the node")
    augument: dict | None = Field(None, title="Augument of the node")
    description: str = Field(None, title="Description of the node")


class Edge(BaseModel):
    """
    Edge class for the flowchart

    Attributes:
        id (str): ID of the edge
        source (str): Source of the edge
        target (int): Target of the edge
        condition (bool): Condition of the edge
        description (str): Description of the edge
    """

    id: int = Field(default=0, title="ID of the edge")
    source: str | None = Field(None, title="Source of the edge")
    target: int | None = Field(None, title="Target of the edge")
    condition: bool | None = Field(None, title="Condition of the edge")
    description: str = Field(None, title="Description of the edge")


class Flowchart(BaseModel):
    """
    Flowchart class for the flowchart

    Attributes:
        nodes (list[Node]): List of nodes in the flowchart
        edges (list[Edge]): List of edges in the flowchart
        current_node (int): Current node in the flowchart
        return_value (dict): Return value of the node
        variables (dict): Variables in the flowchart
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
