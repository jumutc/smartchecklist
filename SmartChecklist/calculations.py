import re
from nltk.corpus.reader.wordnet import WordNetError
from nltk.tokenize.punkt import  PunktSentenceTokenizer
from SmartChecklist.taggers import *
from nltk.corpus import wordnet as wn

#tagger
tagger = get_hunpos_tagger()

#hardcode: excluded WordNet categories
excluded = ['entity', 'physical_entity', 'abstraction', 'relation', 'part', 'thing',
            'substance', 'matter', 'solid', 'group', 'object', 'whole', 'artifact', 'organism']

#constants
noun = '\.n\.\d+'
sub = '.n.01'
sub2 = '.n.02'
score = '_'
tagIN = 'IN'
tagCC = 'CC'
tagCD = 'CD'
tagRB = 'RB'
tagVB = 'VB'
tagNN = 'NN'
tagJJ = 'JJ'
tagVBN = 'VBN'
tagVBP = 'VBP'
tagNNS = 'NNS'
tagNone = 'None'
punctuation = [',', '.', ';', '!', '?', ':']


def supported_tag(tag): return tag == tagNN or tag == tagNNS


def unsupported_tag(tag): return tag.startswith(tagNN) and not supported_tag(tag)


def supported_additional_tag(tag, include_custom): return tag == tagNone or (
    include_custom and (tag == tagIN or tag == tagCD or tag == tagJJ or tag == tagVBN))


def get_punctuation_index(tokens, ind, to_ind):
    def p_map(el): return 1 if el in punctuation else 0

    p_indices = map(p_map, tokens[ind:to_ind])
    first_punctuation_ind = len(p_indices) - p_indices.index(1) if 1 in p_indices else -1

    return to_ind if first_punctuation_ind == -1 else to_ind - first_punctuation_ind


def get_words_unsupported(text):
    def_tags = nltk.pos_tag(nltk.word_tokenize(text))
    return [word.lower() for (word, tag) in def_tags if unsupported_tag(tag)]


def consolidate_by_nouns(words, tags):
    prepositions = [word for (word, tag) in tags if tag == tagIN]
    nouns = [word for (word, tag) in tags if supported_tag(tag)]
    consolidated = list()
    start_ind = 0
    curr_ind = -1

    for word in words:
        curr_ind += 1
        if word in nouns:
            consolidated.append(' '.join(words[start_ind:curr_ind + 1]))
            start_ind = curr_ind + 1

    curr_ind = 0
    for item in consolidated:
        parts = item.split(' ')
        if parts[0] in prepositions and curr_ind != 0:
            prev_item = consolidated[curr_ind - 1]
            consolidated[curr_ind - 1] = ' '.join([prev_item, item])
            consolidated.remove(item)
        curr_ind += 1

    return consolidated


def tag_nouns(text, create_map, include_custom):
    tags = tagger.tag(nltk.word_tokenize(text.lower()))
    words = [word for (word, tag) in tags if supported_tag(tag) or supported_additional_tag(tag, include_custom)]

    if include_custom:
        words = consolidate_by_nouns(words, tags)

    if create_map:
        tagged_words = {}
        for (word, tag) in tags:
            if word in words:
                tagged_words[word] = tag

        return tagged_words

    return [word.lower() for word in words]


def get_todo_items(text):
    all_items = list()
    tokenizer = PunktSentenceTokenizer()
    sen_tokens = tokenizer.tokenize(text)

    for sen_token in sen_tokens:
        todo_items = list()
        tokens = nltk.word_tokenize(sen_token)

        tags = tagger.tag(tokens)
        stop_words = [word for (word, tag) in tags if tag in (tagVB, tagVBP)]

        ind = -1
        for word in stop_words:
            curr_ind = tokens.index(word)
            if curr_ind != 0 and tags[curr_ind - 1][1] in (tagCC, tagRB):
                to_ind = curr_ind - 1
            else: to_ind = curr_ind
            if ind != -1 and abs(to_ind - ind) > 1:
                todo_items.append(' '.join(tokens[ind:get_punctuation_index(tokens, ind, to_ind)]))
            elif ind != -1 and len(todo_items) > 0:
                last_ind = len(todo_items)
                todo_items[last_ind - 1] = ' '.join([todo_items[last_ind - 1], tokens[to_ind - 1]])
            ind = curr_ind

        if ind != -1 and abs(len(tokens) - ind) > 1:
            todo_items.append(' '.join(tokens[ind:get_punctuation_index(tokens, ind, len(tokens))]))
        elif ind != -1 and len(todo_items) > 0:
            last_ind = len(todo_items)
            todo_items[last_ind - 1] = ' '.join([todo_items[last_ind - 1], tokens[len(tokens) - 1]])

        all_items.extend(todo_items)

    return all_items


def join_numbers(sen_tokens):
    ind = 0
    max_tokens = len(sen_tokens)
    for token in sen_tokens:
        if ind > 0 and ind + 1 < max_tokens and token in punctuation and sen_tokens[ind - 1].isdigit() and re.match('\d+', sen_tokens[ind + 1]):
            num_rec = ''.join(sen_tokens[ind - 1:ind + 2])
            if ind + 1 < max_tokens and sen_tokens[ind + 1] not in punctuation:
                sen_tokens[ind + 1] = num_rec
            elif ind + 1 >= max_tokens or sen_tokens[ind + 1] in punctuation:
                sen_tokens.insert(ind + 1, num_rec)
        ind += 1


def get_delimited_items(text):
    delimited_items = list()
    sen_tokens = re.split('([;.,?!:]+)', text)
    join_numbers(sen_tokens)

    if len(sen_tokens) > 0 and sen_tokens[0] == text:
        return get_checklist(text)

    for sen_token in sen_tokens:
        tokens = nltk.word_tokenize(sen_token)
        tags = nltk.pos_tag(tokens)

        #escape numbers and punctuation alone
        if len(tags) == 1 and (tags[0][0] in punctuation or tags[0][0].isdigit()):
            continue

        ind = 0
        delimit_ind = -1
        for (word, tag) in tags:
            if tag in punctuation or tag == tagCC:
                delimited_items.append(' '.join(tokens[delimit_ind + 1:ind]))
                delimit_ind = ind
            ind += 1

        if ind != -1 and abs(len(tokens) - delimit_ind) > 1:
            delimited_items.append(' '.join(tokens[delimit_ind + 1:len(tokens)]))

    return delimited_items


def get_checklist(text):
    return tag_nouns(text, False, True)


def categorize(text):
    tree = {}
    all_words = {}
    categorized = {}
    not_categorized = {}
    tagged_words = tag_nouns(text, True, False)

    def m(list): return [re.sub(noun, '', syn.name) for syn in list]

    def m_(list): return [re.sub(score, ' ', name) for name in list if name not in excluded]

    def create_tree(list):
        if not len(list):
            return None
        else:
            key = list.pop(0)
            return {key: create_tree(list)}

    def expand_tree(tree, list):
        if not len(list): return tree
        if tree.has_key(list[0]):
            key = list.pop(0)
            inner_tree = tree[key]
            if inner_tree is not None:
                inner_tree.update(expand_tree(inner_tree, list))
            elif len(list):
                tree[key] = create_tree(list)
            return tree
        else:
            return create_tree(list)

    def trace_tree(tree, node_found):
        inner_list = list()
        for key, item in tree.items():
            if (item is not None and len(item) > 1) or node_found:
                if item is not None: inner_list.extend(trace_tree(item, True))
                inner_list.append(key)
        return inner_list

    def trace_tree_lite(tree, items_to_find):
        inner_list = list()
        for key, item in tree.items():
            if item is None and key in items_to_find:
                inner_list.append(key)
            elif type(item) is dict:
                inner_list.extend(trace_tree_lite(item, items_to_find))
                if len(inner_list) > 0: inner_list.append(key)
        return inner_list

    for word in tagged_words.keys():
        try:
            not_categorized[word] = list()
            set = wn.synset(word + sub).hypernym_paths()
            not_categorized[word].extend(map(m_, map(m, set)))
            set2 = wn.synset(word + sub2).hypernym_paths()
            not_categorized[word].extend(map(m_, map(m, set2)))
        except WordNetError as str_err:
            print "WordNet error: {0}".format(str_err)
        try:
            if tagged_words[word] == tagNNS:
                escaped = word.rstrip('s')
                set = wn.synset(escaped + sub).hypernym_paths()
                not_categorized[word].extend(map(m_, map(m, set)))
                set2 = wn.synset(escaped + sub2).hypernym_paths()
                not_categorized[word].extend(map(m_, map(m, set2)))
        except WordNetError as str_err:
            print "WordNet error: {0}".format(str_err)

    for word, paths in not_categorized.items():
        all_words[word] = list()
        for path in paths:
            all_words[word].extend(path)
            tree.update(expand_tree(tree, path))

    all_categories = frozenset(trace_tree(tree, False))
    items_to_find = frozenset(tagged_words) - all_categories

    all_categories = all_categories.union(trace_tree_lite(tree, items_to_find))
    all_categories = all_categories - frozenset(tagged_words)

    for word, paths in not_categorized.items():
        all_by_word = frozenset(all_words[word])
        categorized[word] = list(all_by_word.intersection(all_categories))

    for word in tagged_words.keys():
        if not word in categorized.keys():
            categorized[word] = ['untagged']

    return categorized

