class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, data):
    if not root:
        return Node(data)

    if data < root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)

    return root


def search(root, target):
    if not root:
        return None

    if root.data == target:
        return root

    if target < root.data:
        return search(root.left, target)

    return search(root.right, target)
