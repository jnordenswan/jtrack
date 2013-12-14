def print_tree(tree, depth=0):
    if tree is None or len(tree) == 0:
        print("\t" * depth, "-")
    else:
        for key, val in tree.items():
            print("\t" * depth, key)
            print_tree(val, depth+1)

