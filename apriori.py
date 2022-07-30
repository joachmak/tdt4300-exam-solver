from utils import get_list_str_without_citation_marks, print_itemset, str_to_arr


class Transaction:
    def __init__(self, tid: str, items: list):
        self.tid = tid
        self.items = items

    def __str__(self):
        return f"({self.tid}: {self.items})"


class Rule:
    def __init__(self, left_side: list, right_side: list, conf=None):
        self.left_side = left_side
        self.right_side = right_side
        self.conf = conf

    def __str__(self):
        return f"{get_list_str_without_citation_marks(self.left_side)} -> {get_list_str_without_citation_marks(self.right_side)}"


def join_two_itemsets(itemset_1: list, itemset_2: list, print_output=False):
    result = []
    for item in itemset_1:
        result.append(item)
    for item in itemset_2:
        if item not in result:
            result.append(item)
    if print_output:
        print(f"{get_list_str_without_citation_marks(itemset_1)} U {get_list_str_without_citation_marks(itemset_2)} = {get_list_str_without_citation_marks(result)}")
    return result


def apriori_gen_f_k_1_X_f_1(f_k_1: list, f_1: list):
    """
    Args: f_(k-1): the frequent k-1 itemset. f_1: the frequent 1-itemset. Both arguments are lists of python sets
    """
    print(f"We combine the frequent {len(f_k_1[0])}-itemset")
    print_itemset(f_k_1)
    print("with the frequent 1-itemset")
    print_itemset(f_1)
    print("and obtain")
    new_itemsets = []
    for frequent_k_itemset in f_k_1:
        for frequent_1_itemset in f_1:
            if frequent_1_itemset[0] in frequent_k_itemset:
                continue
            new_itemset = set(frequent_k_itemset + frequent_1_itemset)
            add_new_itemset = True
            for itemset in new_itemsets:
                # convert to sets
                if set(itemset) == new_itemset:
                    add_new_itemset = False
                    break
            if add_new_itemset:
                new_itemsets.append(frequent_k_itemset + frequent_1_itemset)
    # remove duplicates
    result = []
    [result.append(x) for x in new_itemsets if x not in result]
    return result


def apriori_gen_f_k_1_X_f_k_1(f_k_1: list, print_stuff=True):
    if print_stuff:
        print("We use the F_(k-1) x F_(k-1) method to generate candidate itemsets from the frequent itemsets.")
    candidate_itemsets = []
    k = len(f_k_1[0]) + 1
    if k == 2:
        if print_stuff:
            print(f"We set k = k+1 = 2. Since k=2, the F_(k-1) x F_(k-1) method will generate the candidate itemsets "
              f"by just combining all combinations of items.")
    for i in range(len(f_k_1)):
        for j in range(i + 1, len(f_k_1)):
            if i == j:
                continue
            f_1 = f_k_1[i]
            f_2 = f_k_1[j]
            # Check if the first k-2 items are equal
            equal_first_items = True
            for m in range(k - 2):
                if f_1[m] != f_2[m]:
                    equal_first_items = False
                    break
            if equal_first_items:
                # join and print output to console if k!=2 (when the output is quite uninteresting)
                new_itemset = join_two_itemsets(f_1, f_2, k != 2)
                new_itemset.sort()
                if new_itemset not in candidate_itemsets:
                    candidate_itemsets.append(new_itemset)
    # remove duplicate itemsets
    i = 0
    while i < len(candidate_itemsets):
        itemset = candidate_itemsets[i]
        removed_itemset = False
        for j in range(i + 1, len(candidate_itemsets)):
            itemset_2 = candidate_itemsets[j]
            if set(itemset) == set(itemset_2):
                candidate_itemsets.remove(itemset)
                removed_itemset = True
        if not removed_itemset:
            i += 1
    candidate_itemsets.sort()
    return candidate_itemsets


def prune_infrequent_itemsets(itemsets, transactions, minsup_count):
    """ minsup_count = minimum number of transactions that the itemset must be present in to remain unpruned """
    frequent_itemsets = []
    for itemset in itemsets:
        sup_count = 0
        transaction_list = []
        for transaction in transactions:
            itemset_in_transaction = True
            for elem in itemset:
                if elem not in transaction.items:
                    itemset_in_transaction = False
                    break
            if itemset_in_transaction:
                sup_count += 1
                transaction_list.append(transaction.tid)
        print_str = f"{get_list_str_without_citation_marks(itemset)}: sup-count {sup_count}"
        if len(transaction_list) > 0:
            print_str += f" (transactions {get_list_str_without_citation_marks(transaction_list)})"
        print(print_str + f" {'...✓' if sup_count >= minsup_count else '...x'}")
        if sup_count >= minsup_count:
            frequent_itemsets.append(itemset)
    return frequent_itemsets


def get_all_frequent_1_itemsets(transactions, minsup_count):
    # get all items
    print("We get all frequent 1-itemsets.")
    items = {}
    for transaction in transactions:
        for char in transaction.items:
            if char in items:
                items[char] += 1
                continue
            items[char] = 1
    print(items)
    infrequent_itemsets = []
    for item in items:
        if items[item] < minsup_count:
            infrequent_itemsets.append(item)
    for item in infrequent_itemsets:
        items.pop(item)
    print(
        f"We prune the infrequent itemsets with support count below {minsup_count}: {get_list_str_without_citation_marks(infrequent_itemsets)}, "
        f"and we are left with {get_list_str_without_citation_marks(list(items.keys()))}\n"
    )
    # Convert to list
    result = []
    for item in items:
        result.append(list(item))
    result.sort()
    return result


def apriori_frequent_itemset_gen(transactions, minsup_count):
    f_k = get_all_frequent_1_itemsets(transactions, minsup_count)
    all_frequent_itemsets = [] + f_k
    k = 1
    while len(f_k) > 1:
        k += 1
        c_k = apriori_gen_f_k_1_X_f_k_1(f_k)
        print("We get the following candidate itemsets:")
        f_k = prune_infrequent_itemsets(c_k, transactions, minsup_count)
        all_frequent_itemsets += f_k
        print("Frequent itemsets are marked with a '✓', while the ones marked with 'x' are discarded.\n")
    print("All frequent itemsets:")
    print_itemset(all_frequent_itemsets)
    return all_frequent_itemsets


def get_itemset_sup_count(itemset, transactions):
    sup_count = 0
    for transaction in transactions:
        increment_sup_count = True
        for item in itemset:
            if item not in transaction.items:
                increment_sup_count = False
                break
        sup_count += 1 if increment_sup_count else 0
    return sup_count


def calculate_conf(rule, transactions, minconf):
    nominator = [] + rule.left_side + rule.right_side
    denominator = [] + rule.left_side
    nominator_sup_count = get_itemset_sup_count(nominator, transactions)
    denominator_sup_count = get_itemset_sup_count(denominator, transactions)
    conf = round(nominator_sup_count / denominator_sup_count, 3)
    rule.conf = conf
    print(f"confidence of {str(rule)}: σ({get_list_str_without_citation_marks(nominator)}) / "
          f"σ({get_list_str_without_citation_marks(denominator)}) = {conf} {'...✓' if conf > minconf else '...x'}")
    return conf


def generate_rules_for_single_itemset(itemset, transactions, minconf):
    print(f"We generate rules for the itemset {get_list_str_without_citation_marks(itemset)}.")
    print(f"First, we generate the rules with 1-consequents and prune those whose confidence is too low (<{minconf}):")
    k = len(itemset)
    m = 1
    rules = []
    m_item_consequents = []
    for consequent in itemset:
        left_side = [x for x in itemset if x not in consequent]
        rule = Rule(left_side, list(consequent))
        conf = calculate_conf(rule, transactions, minconf)
        if conf >= minconf:
            rules.append(rule)
            m_item_consequents.append(consequent)
    print(f"\nWe then find all 2-consequents, ..., m-consequents until len({itemset}) > m + 1.")
    print(f"Since len({itemset}) = {len(itemset)}, we stop at {k - 1}-consequents.")
    while k > m + 1:
        print(f"Generating rules with {m + 1}-consequents:")
        print(f"We use the apriori-gen algorithm, combining the set of {m}-consequents with high enough confidence (>={minconf}).")
        new_consequents = apriori_gen_f_k_1_X_f_k_1(m_item_consequents, False)
        m_item_consequents = []
        for consequent in new_consequents:
            left_side = [x for x in itemset if x not in consequent]
            rule = Rule(left_side, consequent)
            conf = calculate_conf(rule, transactions, minconf)
            if conf >= minconf:
                rules.append(rule)
                m_item_consequents.append(consequent)
        m += 1
    print(f"\nFinal set of rules:")
    for rule in rules:
        print(f"{str(rule)}, confidence: {round(rule.conf * 100, 1)}%")


def main():
    transactions = [
        Transaction("1", str_to_arr("ABCD")),
        Transaction("2", str_to_arr("ACDF")),
        Transaction("3", str_to_arr("ACDEG")),
        Transaction("4", str_to_arr("ABDF")),
        Transaction("5", str_to_arr("BCG")),
        Transaction("6", str_to_arr("DFG")),
        Transaction("7", str_to_arr("ABG")),
        Transaction("8", str_to_arr("CDFG")),
        #Transaction("T7", str_to_arr("ABG")),
        #Transaction("T8", str_to_arr("CDFG")),
    ]
    #minconf = 0.75
    minsup_count = 3
    apriori_frequent_itemset_gen(transactions, minsup_count)
    #frequent_itemset = ['A', 'B', 'H']
    #print("\n")
    #generate_rules_for_single_itemset(frequent_itemset, transactions, minconf)


if __name__ == "__main__":
    main()
