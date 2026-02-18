class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        return root

    def search(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            return self.search(root.left, key)

        return self.search(root.right, key)


if __name__ == "__main__":
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for v in values:
        bst.root = bst.insert(bst.root, v)

    result = bst.search(bst.root, 60)
    print("Found" if result else "Not Found")
