from decimal import Decimal
from SmartChecklist.models import HistogramItem, CheckList, DictionaryItem

def create_all_items(all_items, item):
    histogram_items = []
    for over_item in all_items:
        if over_item.id != item.id:
            histogram_item = HistogramItem()
            histogram_item.item_a = item
            histogram_item.item_b = over_item
            histogram_items.append(histogram_item)
            histogram_item.save()

    return histogram_items


def calculate_histogram(checklist):
    histogram_items = []

    def m(x): return x.item_b

    cnt = len(CheckList.objects.all())

    for item in DictionaryItem.objects.all():
        filtered = HistogramItem.objects.filter(item_a=item).all()
        found = map(m, filtered)

        all_items = [x for x in checklist.items.all() if x not in found and x is not item]
        new_items = create_all_items(all_items, item)

        histogram_items.extend(new_items)
        histogram_items.extend(filtered)

        for filtered_item in filtered:
            add_num = 1 if filtered_item.item_a in checklist.items.all() else 0
            filtered_item.probability = Decimal(Decimal(cnt) * filtered_item.probability + add_num) / Decimal(cnt + 1)
            filtered_item.save()

    return histogram_items


def calculate_probabilities(checklist):
    filtered = HistogramItem.objects.filter(item_b__in=checklist.items.all()).all()

    def r(x, y): return x * y.probability

    def m(x): return x.item_a

    a_items = set(map(m, filtered))
    probabilities = {}

    for item in a_items:
        def f(x): return x.item_a == item

        seq = filter(f, filtered)
        probabilities[item.name] = reduce(r, seq, 1)

    return probabilities
