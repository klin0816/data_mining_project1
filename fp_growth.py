from collections import defaultdict, namedtuple
import sys
import ast
import itertools
import pprint


def find_frequent_itemsets(transactions, minimum_support, include_support=False):
    items = defaultdict(lambda: 0) # mapping from items to their supports

    for transaction in transactions:
        for item in transaction:
            items[item] += 1

    items = dict((item, support) for item, support in items.items()
        if support >= minimum_support)

    def clean_transaction(transaction):
        transaction = sorted((v for v in transaction if v in items), reverse=True, key=lambda v:items[v])
        return transaction

    master = FPTree()
    for transaction in map(clean_transaction, transactions):
        master.add(transaction)

    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                # New winner!
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s # pass along the good news to our caller

    for itemset in find_with_suffix(master, []):
        yield itemset

class FPTree(object):
    Route = namedtuple('Route', 'head tail')
    def __init__(self):
        self._root = FPNode(self, None, None)
        self._routes = {}
    @property
    def root(self):
        return self._root
    def add(self, transaction):
        point = self._root
        for item in transaction:
            next_point = point.search(item)
            if next_point:
                next_point.increment()
            else:
                next_point = FPNode(self, item)
                point.add(next_point)
                self._update_route(next_point)
            point = next_point
    def _update_route(self, point):
        assert self is point.tree
        try:
            route = self._routes[point.item]
            route[1].neighbor = point # route[1] is the tail
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))


def conditional_tree_from_paths(paths):
    tree = FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None

    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    return tree

class FPNode(object):
    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):
        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self
    def search(self, item):
        try:
            return self._children[item]
        except KeyError:
            return None
    def __contains__(self, item):
        return item in self._children
    @property
    def tree(self):
        return self._tree
    @property
    def item(self):
        return self._item
    @property
    def count(self):
        return self._count
    def increment(self):
        self._count += 1
    @property
    def root(self):
        return self._item is None and self._count is None
    @property
    def leaf(self):
        return len(self._children) == 0
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value
    @property
    def neighbor(self):
        return self._neighbor
    @neighbor.setter
    def neighbor(self, value):
        self._neighbor = value
    @property
    def children(self):
        return tuple(self._children.itervalues())


if __name__ == '__main__':
    minsup_rate = sys.argv[2]
    min_confidence = float(sys.argv[3])
    full_list = []
    with open(sys.argv[1], 'r') as database:
        transactions = ast.literal_eval(database.read())
        transactions_num = 0
        for aa in transactions:
            transactions_num += 1
            for bb in aa:
                if bb not in full_list:
                    full_list.append(bb)
        minsup = float(minsup_rate) * float(transactions_num)
        full_list.sort()
        result = []

        for itemset, support in find_frequent_itemsets(transactions, minsup, True):
            result.append((itemset,support))
        
        result = sorted(result, key=lambda i: i[0])
        full_dict = {}
        for itemset, support in result:
            full_dict[tuple(itemset)] = support
        support_confidence = {}

        for r in range(2, len(full_list)+1):
            for itemset, support in result:
                if len(itemset) == r:
                    for r2 in range(1, len(itemset)):
                        for ccc in itertools.combinations(itemset, r2):
                            ddd = set(itemset[:])
                            cc = set(ccc)
                            if set(ccc).issubset(ddd):
                                ddd = ddd - cc
                                stt = str(cc) + '->' + str(ddd)
                                if stt not in support_confidence:
                                    support_confidence[stt] = {'#SUP': support}
                                else:
                                    support_confidence[stt]['#SUP'] += 1
                                support_confidence[stt]['#CONF'] = float(support_confidence[stt]['#SUP'] / full_dict[ccc])
	
        for key in list(support_confidence.keys()):
            if support_confidence[key]['#CONF'] < min_confidence:
                del support_confidence[key] 
        pprint.pprint(support_confidence)
