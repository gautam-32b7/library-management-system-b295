# Node 
class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

# BST
class BST:
    def __init__(self):
        self.root = None

    # Insert a book into the BST based on the ISBN
    def insert(self, book):
        if self.root is None:
            self.root = Node(book)
        else:
            self._insert(self.root, book)
    
    def _insert(self, current_node, book):
        if book.isbn < current_node.book.isbn:
            if current_node.left is None:
                current_node.left = Node(book)
            else:
                self._insert(current_node.left, book)
        elif book.isbn > current_node.book.isbn:
            if current_node.right is None:
                current_node.right = Node(book)
            else:
                self._insert(current_node.right, book)
        else:
            print("Book with is ISBN already exists in the BST")
    
    # Search for a book in the BST based on ISBN
    def search(self, isbn):
        return self._search(self.root, isbn)

    def _search(self, current_node, isbn):
        if current_node is None:
            return None
        if isbn == current_node.book.isbn:
            return current_node.book
        elif isbn < current_node.book.isbn:
            return self._search(current_node.left, isbn)
        else:
            return self._search(current_node.right, isbn)
        
    # In-order traversal (sorted by ISBN)
    def inorder_traversal(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books
    
    def _inorder_traversal(self, current_node, books):
        if not current_node:
            return
        self._inorder_traversal(current_node.left, books)
        books.append(current_node.book)
        self._inorder_traversal(current_node.right, books)
