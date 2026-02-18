class Node:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None


def inorder(node):
    if node is None:
        return []

    values = []
    values += inorder(node.left)
    values.append(node.x)
    values += inorder(node.right)

    return values

print("File executed")
