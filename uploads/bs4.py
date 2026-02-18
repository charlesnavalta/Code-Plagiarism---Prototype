class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert_value(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, current, value):
        if current is None:
            return Node(value)

        if value < current.val:
            current.left = self._insert(current.left, value)
        else:
            current.right = self._insert(current.right, value)

        return current

    def contains(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False

        if node.val == value:
            return True

        if value < node.val:
            return self._search(node.left, value)

        return self._search(node.right, value)
