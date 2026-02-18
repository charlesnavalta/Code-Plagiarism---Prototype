class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def inorder_traversal(root):
    if root is None:
        return []

    result = []
    result.extend(inorder_traversal(root.left))
    result.append(root.value)
    result.extend(inorder_traversal(root.right))

    return result

if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    print(inorder_traversal(root))
