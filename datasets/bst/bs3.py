class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def add(self, node, value):
        if node is None:
            return TreeNode(value)

        if value < node.value:
            node.left = self.add(node.left, value)
        else:
            node.right = self.add(node.right, value)

        return node

    def find(self, node, value):
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self.find(node.left, value)

        return self.find(node.right, value)
