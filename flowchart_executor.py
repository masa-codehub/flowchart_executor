import json

class FlowchartExecutor:
    def __init__(self, flowchart_json):
        self.flowchart = json.loads(flowchart_json)
        self.nodes = {node['id']: node for node in self.flowchart['nodes']}
        self.current_node = None
        self.variables = {}
        self.node_executors = {
            'start': self.execute_start,
            'process': self.execute_process,
            'decision': self.execute_decision,
            'loop': self.execute_loop,
            'end': self.execute_end
        }

    def execute(self):
        self.current_node = self.find_start_node()
        if not self.current_node:
            print("Start node not found.")
            return
        while self.current_node['type'] != 'end':
            self.execute_node(self.current_node)
            self.current_node = self.find_next_node()
            if not self.current_node:
                print("Next node not found, terminating execution.")
                break

    def find_start_node(self):
        return next((node for node in self.nodes.values() if node['type'] == 'start'), None)

    def execute_node(self, node):
        node_type = node['type']
        if node_type in self.node_executors:
            self.node_executors[node_type](node)
        else:
            print(f"Unknown node type: {node_type}")

    def execute_start(self, node):
        print(f"Starting execution: {node['text']}")

    def execute_process(self, node):
        print(f"Executing process: {node['text']}")

    def execute_decision(self, node):
        print(f"Decision: {node['text']}")
        return True  # 仮の実装として、常にTrueを返す

    def execute_loop(self, node):
        print(f"Executing loop: {node['text']}")
        self.variables[node['initialization'].split('=')[0].strip()] = int(node['initialization'].split('=')[1].strip())
        while eval(node['condition'], self.variables):
            for sub_node_id in node['body']:
                self.execute_node(self.nodes[sub_node_id])
            exec(node['increment'], self.variables)

    def execute_end(self, node):
        print(f"Ending execution: {node['text']}")

    def find_next_node(self):
        for edge in self.flowchart['edges']:
            if edge['from'] == self.current_node['id']:
                if 'condition' not in edge or self.execute_decision(self.current_node) == (edge['condition'] == 'Yes'):
                    return self.nodes.get(edge['to'])
        return None