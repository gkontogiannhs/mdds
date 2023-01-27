class MBRNode:
    def __init__(self, min_entries, max_entries, parent=None):
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.children = []
        self.points = []
        self.mbr = None
        self.parent = parent


    def add_point(self, point):
        self.points.append(point)
        self.update_mbr()


    def is_leaf(self):
        return not self.children


    def is_overfull(self):
        return len(self.points) > self.max_entries


    def get_leaf_for_point(self, point):

        """
        Traverse the R-tree top-down, starting from the root, at each level
        - If there is a node whose directory rectangle contains the point to be inserted, then search the subtree
        - Else choose a node such that the enlargement of its directory rectangle is minimal, then search the subtree
        """

        if self.is_leaf():
            return self
        else:
            return min(self.children, key=lambda node: node.get_mbr_enlargement(point)).get_leaf_for_point(point)


    def get_mbr_enlargement(self, point):

        if not self.mbr: 
            return float('inf')
        else:
            return self.mbr.get_enlargement(Rectangle(point[0], point[1], point[0], point[1]))


    def get_nodes_for_point(self, point):
        if self.is_leaf():
            return [self]
        else:
            nodes = []
            for child in self.children:
                if child.mbr is not None and child.mbr.contains_point(point):
                    nodes.extend(child.get_nodes_for_point(point))
            return nodes


    def update_children(self, old_child, new_child1, new_child2):
        self.children.remove(old_child)
        self.children.append(new_child1)
        self.children.append(new_child2)
        self.update_mbr()


    def linear_split(self):
        if self.is_leaf():
            # Divide the overflowing leaf node into two groups:
            # group1 will contain roughly half of the entries
            # group2 will contain the remaining entries
            group1, group2 = self.divide_into_two_groups()
            
            # Create two new leaf nodes from the two groups
            new_node1 = MBRNode(self.min_entries, self.max_entries, parent=self)
            new_node1.points = group1
            new_node2 = MBRNode(self.min_entries, self.max_entries, parent=self)
            new_node2.points = group2
            
            # Update the parent's children list
            if self.parent:
                self.parent.update_children(self, new_node1, new_node2)


    def divide_into_two_groups(self):
        """Divides the overflowing leaf node into two groups"""
        # Sort the points by their x-coordinates
        self.points.sort(key=lambda point: point[0])
        # Calculate the split index
        median = len(self.points) // 2
        # Divide the points into two groups
        group1 = self.points[:median]
        group2 = self.points[median+1:]
        return group1, group2


    def quadratic_split(self):
        if self.is_leaf():
            seeds = self.get_seeds()
            
            new_node1 = MBRNode(self.min_entries, self.max_entries, parent=self)
            new_node1.add_point(seeds[0])
            
            new_node2 = MBRNode(self.min_entries, self.max_entries, parent=self)
            new_node2.add_point(seeds[1])
            
            remaining_points = [point for point in self.points if point != seeds[0] and point != seeds[1]]
            
            while len(remaining_points) > 0:
                current_point = remaining_points.pop(0)
                chosen_node = min(new_node1, new_node2, key=lambda node: node.get_mbr_enlargement(current_point))
                chosen_node.add_point(current_point)
            
            self.children = [new_node1, new_node2]
            self.points = []
            
            if self.parent is not None:
                self.parent.update_children(self, new_node1, new_node2)
                self.parent.update_mbr()


    def add_point_to_best_node(self, point, node1, node2):
        enlargement1 = node1.get_mbr_enlargement(point)
        enlargement2 = node2.get_mbr_enlargement(point)

        if enlargement1 < enlargement2:
            node1.add_point(point)
        else:
            node2.add_point(point)


    def get_seeds(self):

        candidates = self.children if self.children else self.points

        max_waste = -1
        seeds = []

        for i in range(len(candidates)):
            for j in range(i+1, len(candidates)):
                waste = self.get_waste(candidates[i], candidates[j])
                if waste > max_waste:
                    max_waste = waste
                    seeds = [candidates[i], candidates[j]]

        return seeds


    def get_waste(self, c1, c2):
        if isinstance(c1, tuple):
            c1 = Rectangle(c1[0], c1[1], c1[0], c1[1])
            c2 = Rectangle(c2[0], c2[1], c2[0], c2[1])

        combined_rect = c1.combine(c2)
        return combined_rect.get_area() - c1.get_area() - c2.get_area()
        # return c1.get_enlargement(c2)


    def update_mbr(self):
        
        if self.is_leaf():
            x_coords = [point[0] for point in self.points]
            y_coords = [point[1] for point in self.points]

            x1, y1, x2, y2 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)

        else:
            x1, x2 = self.children[0].mbr.x1, self.children[0].mbr.x2
            y1, y2 = self.children[0].mbr.y1, self.children[0].mbr.y2

        for child in self.children:
            x1, x2 = min(x1, child.mbr.x1), max(x2, child.mbr.x2)
            y1, y2 = min(y1, child.mbr.y1), max(y2, child.mbr.y2)

        self.mbr = Rectangle(x1, y1, x2, y2)


    def combine_with_siblings(self):
        if self.parent is None:
            return
        parent = self.parent
        if len(parent.children) < 2 * self.min_entries:
            # Combine this node with all its siblings
            parent.children = [child for child in parent.children if child != self]
            for sibling in parent.children:
                for point in sibling.points:
                    self.add_point(point)
                for child in sibling.children:
                    self.children.append(child)
            parent.update_mbr()
            parent.combine_with_siblings()


class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        
    def get_area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def combine(self, other):

        x1 = min(self.x1, other.x1)
        y1 = min(self.y1, other.y1)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)

        return Rectangle(x1, y1, x2, y2)

    def get_enlargement(self, other):
        if self.intersects(other):
            return 0
        else:
            combined = self.combine(other)
            return combined.get_area() - self.get_area()
    
    def contains_point(self, point):
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2
        

class RTree:
    def __init__(self, min_entries=2, max_entries=4):
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.root = MBRNode(self.min_entries, self.max_entries, parent=None)

    def insert(self, point):
        leaf = self.root.get_leaf_for_point(point)
        leaf.add_point(point)
        
        if leaf.is_overfull():
            leaf.linear_split()

        elif len(leaf.points) < leaf.min_entries:
            leaf.combine_with_siblings()

    def range_search(self, rectangle):
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
