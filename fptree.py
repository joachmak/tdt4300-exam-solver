from tabulate import tabulate

import utils


class Transaction:
    def __init__(self, tid: str, items: list):
        self.tid = tid
        self.items = items

    def __str__(self):
        return f"({self.tid}: {self.items})"


class Item:
    def __init__(self, id, supcount):
        self.id = id
        self.supcount = supcount

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.__str__() + ": " + str(self.supcount)

    def __lt__(self, other):
        return self.supcount < other.supcount


def arr_to_str(arr: list):
    res = ""
    for elem in arr:
        res += elem
    return res


def generate_supcount_table(transactions: list, minsup_count: int):
    supcounts = {}
    for transaction in transactions:
        for elem in transaction.items:
            if elem in supcounts:
                supcounts[elem] += 1
            else:
                supcounts[elem] = 1
    supcount_arr = []
    for key in supcounts:
        if supcounts[key] >= minsup_count:
            supcount_arr.append(Item(key, supcounts[key]))
        else:
            print(f"We don't include {key} because it has support count {supcounts[key]} < {minsup_count} and will "
                  f"therefore not contribute to generating frequent itemsets.")
    s = sorted(supcount_arr, key=lambda x: x.id, reverse=False)
    s = sorted(s, key=lambda x: x.supcount, reverse=True)
    headers = ["Item", "Support count"]
    rows = [[item.id, item.supcount] for item in s]
    # rearrange transactions
    transaction_headers = ["tid", "items"]
    transaction_rows = []
    for transaction in transactions:
        items = transaction.items
        new_items = []
        for item in s:
            if item.id in items:
                new_items.append(item.id)
        transaction.items = new_items
        transaction_rows.append([transaction.tid, arr_to_str(transaction.items)])
    print("\n1-itemsets reordered based on support values: ")
    print(tabulate(rows, headers=headers))
    print("\nReordered transaction table: ")
    print(tabulate(transaction_rows, headers=transaction_headers))


def main():
    transactions = [
        Transaction("t1", utils.str_to_arr("ACDEF")),
        Transaction("t2", utils.str_to_arr("ABCDE")),
        Transaction("t3", utils.str_to_arr("BCF")),
        Transaction("t4", utils.str_to_arr("ACDEF")),
        Transaction("t5", utils.str_to_arr("DB")),
    ]
    generate_supcount_table(transactions, 3)


if __name__ == "__main__":
    main()
