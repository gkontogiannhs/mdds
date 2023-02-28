"""
    The R-Tree implementation above uses an MBRNode class to represent each node in the tree. Each node contains a minimum bounding
    rectangle (MBR) that encloses all the points or child nodes in the subtree rooted at that node. The nodes are split using the
    linear split algorithm, which tries to distribute the points or child nodes evenly among two new child nodes by iteratively
    finding the split axis that yields the minimum overlap between the resulting MBRs. 

    The implementation supports point insertion and range search queries. When a point is inserted, the algorithm first finds
    the leaf node where the point should be inserted using a recursive descent from the root. If the leaf node becomes overfull,
    it is split into two nodes. If the number of points in a leaf node falls below a certain threshold, it may be combined with
    its siblings to reduce the height of the tree. 

    During a range search query, the algorithm starts from the root node and descends recursively through the tree,
    checking whether the MBR of each node intersects the query rectangle. If the node is a leaf node, it checks each point
    in the node to see if it falls within the query rectangle. If the node is an internal node and its MBR intersects the
    query rectangle, it recursively visits all of its child nodes. The algorithm returns a list of all points that fall
    within the query rectangle.
"""       

from mdds.trees.nodes import MBRNode
from mdds.geometry import Rectangle
class RTree:
    def __init__(self, min_entries=2, max_entries=4):
        """
            Creates an instance of the RTree, and sets the minimum and maximum number of entries allowed in each node.
            It also creates the root node of the tree, which is an instance of the "MBRNode" class.
        """
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.root = MBRNode(self.min_entries, self.max_entries, parent=None)


    def build_tree(self, points):
        for point in points:
            self.insert(point)


    def insert(self, point):
        """
            This method takes a list of points as an argument, and finds the leaf node of the tree where the point should be inserted.
            It adds the point to that leaf node, and if the leaf node becomes overfull, it splits the node to maintain the balance of the tree.
            If the leaf node has less than the minimum number of entries, it combines the node with its siblings.
        """
            
        leaf = self.root.get_leaf_for_point(point)
        leaf.add_point(point)
        
        if leaf.is_overfull():
            leaf.linear_split()

        elif len(leaf.points) < leaf.min_entries:
            leaf.combine_with_siblings()


    def range_search(self, rectangle):
        """
            The range_search method takes a rectangle as an argument, and returns a list of points that are contained within the rectangle.
            It does this by recursively traversing the tree, checking if each node's minimum bounding rectangle (MBR) intersects
            with the search rectangle, and if so, checking the points in the leaf nodes.
        """
        results = []
        self._range_search(rectangle, self.root, results)
        return results
        

    def _range_search(self, rectangle, node, results):
        if node.is_leaf():
            for point in node.points:
                if rectangle.contains_point(point):
                    results.append(point)
            return

        if node.mbr is not None and node.mbr.intersects(rectangle):
            for child in node.children:
                self._range_search(rectangle, child, results)
                

    def exists(self, point):
        """
            The exists method takes a point and returns a Boolean indicating whether the point exists in the tree.
            It creates a rectangle with the point's coordinates as the top-left and bottom-right coordinates,
            and calls the range_search method on this rectangle. It then checks if the point is present in the list
            of points returned by the range_search method.
        """
        x, y = point.x, point.y
        rectangle = Rectangle(x, y, x, y)

        return point in self.range_search(rectangle)


    def delete(self, point):
        """
            This delete method takes in a point and removes it from the tree. It first finds the leaf node(s)
            that contain the point and then checks if that node is now underfull. If it is, the method condenses 
            the tree by removing the underfull nodes and reinserting their points and children until the tree is balanced again.
            It also updates the mbrs all the way up to the root.
        """
        nodes = self.root.get_nodes_for_point(point)
        for node in nodes:
            if point in node.points:
                node.points.remove(point)
                if node.is_leaf() and len(node.points) < self.min_entries:
                    self.condense_tree(node)
                break

        if not nodes: return 
        self.update_mbrs_from_leaf(nodes[0])
    

    def condense_tree(self, leaf):
        nodes = [leaf]
        while leaf.parent is not None:
            parent = leaf.parent
            parent.children.remove(leaf)
            if parent.is_leaf():
                if len(parent.points) >= self.min_entries:
                    break
                else:
                    leaf = parent
                    nodes.append(leaf)
            else:
                if len(parent.children) >= self.min_entries:
                    break
                else:
                    leaf = parent
                    nodes.append(leaf)
        for node in nodes:
            if node.parent is not None:
                node.parent.children.remove(node)
            if node.is_leaf():
                self.leaf_list.remove(node)
        self.reinsert_nodes(nodes)
        

    def reinsert_nodes(self, nodes):
        for node in nodes:
            if node.is_leaf():
                for point in node.points:
                    self.insert(point)
            else:
                for child in node.children:
                    self.insert(child)


    def update_mbrs_from_leaf(self, leaf):
        while leaf.parent is not None:
            leaf.parent.mbr = self.get_mbr_from_children(leaf.parent)
            leaf = leaf.parent


    def get_mbr_from_children(self, node):
        if not node.children:
            return None
        else:
            x1, y1, x2, y2 = node.children[0].mbr.x1, node.children[0].mbr.y1, node.children[0].mbr.x2, node.children[0].mbr.y2
            for child in node.children:
                x1, x2 = min(x1, child.mbr.x1), max(x2, child.mbr.x2)
                y1, y2 = min(y1, child.mbr.y1), max(y2, child.mbr.y2)
            return Rectangle(x1, y1, x2, y2)
