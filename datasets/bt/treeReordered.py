class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def inorder_iterative(root):
    stack = []
    current = root
    output = []

    while current or stack:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        output.append(current.data)
        current = current.right

    return output

print("File executed")
