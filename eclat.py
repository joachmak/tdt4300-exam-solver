from utils import get_list_str_without_citation_marks


class Itemset:
    def __init__(self, itemset: list, tid_set: list):
        self.itemset = itemset
        self.tid_set = tid_set

    def __str__(self):
        return f"{self.itemset}: {get_list_str_without_citation_marks(self.tid_set)}"


def intersect(a: list, b: list):
    result = []
    for elem in a:
        if elem in b:
            result.append(elem)
    #print(f"{a} intersect {b} = {result}")
    return result


def union(a:list, b:list):
    result = []
    for elem in a:
        if elem not in result:
            result.append(elem)
    for elem in b:
        if elem not in result:
            result.append(elem)
    #print(f"{a} union {b} = {result}")
    return result


def print_list(a: list):
    for elem in a:
        print(elem)


def prune_itemsets(itemsets, minsup):
    print(f"\nWe generate all {len(itemsets[0].itemset)}-itemsets:")
    result = []
    for itemset in itemsets:
        is_good = len(itemset.tid_set) >= minsup
        if is_good:
            result.append(itemset)
        print(f"{itemset} {'...✓' if is_good else '...x'}")
    return result


def main():
    itemsets = [
        Itemset(["i1"], ["T100", "T400", "T500", "T700", "T800", "T900"]),
        Itemset(["i2"], ["T100", "T200", "T300", "T400", "T600", "T800", "T900"]),
        Itemset(["i3"], ["T300", "T500", "T600", "T700", "T800", "T900"]),
        Itemset(["i4"], ["T200", "T400"]),
        Itemset(["i5"], ["T100", "T800"]),
    ]
    minsup_count = 2
    print(f"At each step, we combine the itemsets using the union set operator, and take the intersect of their "
          f"transaction sets. Transaction sets with fewer than minsup-count ({minsup_count}) transactions are pruned "
          f"(marked with an 'x'). The rest are kept for the next iteration (marked with a '✓').")
    itemsets = prune_itemsets(itemsets, minsup_count)
    all_frequent_itemsets = [] + itemsets
    while True:
        # generate new itemsets by intersecting 2 and 2 itemsets
        candidate_itemsets = []
        for i in range(len(itemsets)):
            itemset_1 = itemsets[i]
            for j in range(i+1, len(itemsets)):
                itemset_2 = itemsets[j]
                new_itemset_tid_set = intersect(itemset_1.tid_set, itemset_2.tid_set)
                new_itemset = union(itemset_1.itemset, itemset_2.itemset)
                new_itemset_obj = Itemset(new_itemset, new_itemset_tid_set)
                add_itemset = True
                for itemset in itemsets:
                    if set(itemset.itemset) == set(new_itemset) and set(itemset.tid_set) == set(new_itemset_tid_set):
                        add_itemset = False
                        break
                if add_itemset:
                    #print(f"itemset1: {itemset_1} + itemset2: {itemset_2} -> {new_itemset_obj}")
                    candidate_itemsets.append(new_itemset_obj)
        itemsets = prune_itemsets(candidate_itemsets, minsup_count)
        for item in itemsets:
            add_item = True
            for a_item in all_frequent_itemsets:
                if set(item.itemset) == set(a_item.itemset):
                    add_item = False
                    break
            if add_item:
                all_frequent_itemsets.append(item)
        if len(itemsets) == 0:
            break
    print("\nAll itemsets were pruned, so we won't find any more frequent itemsets. All the frequent itemsets are:")
    for itemset in all_frequent_itemsets:
        print(itemset)


if __name__ == "__main__":
    main()
