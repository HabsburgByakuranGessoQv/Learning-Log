#-*- coding: utf-8 -*-

# 随机产生n张扑克
def generate_cards(n):
    import random
    import itertools
    random.seed(1)
    SUITS = 'cdhs'             #四种花色
    RANKS = '23456789TJQKA'    #十三种面值
    DECK = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))
    hand = random.sample(DECK, n)
    return hand

import numpy as np
def crazy_eight(cards):
    trick = {}
    parent = {}
    trick[0] = 1
    parent[0] = None
    print('Computing i={},trick[{}]={},parent[{}]={}'.format(0, 0, trick[0], 0, parent[0]))
    for i, ci in enumerate(cards):
        tem_trick = []
        if i > 0:
            print('Computing i={},ci={}'.format(i, ci))
            for j, cj in enumerate(cards[:i]):
                print('\t j={},cj={}'.format(j, cj))
                if is_trick(ci,cj):
                    tem_trick.append(trick[j])
                    print('\t ci={}~cj={}, trick[{}]={} is appended'.format(ci, cj, j, trick[j]))
                else:
                    tem_trick.append(0)
                    print('\t ci={}<>cj={},0 is appended'.format(ci, cj))
            max_trick = max(tem_trick)
            trick[i] = 1+max_trick
            print('\t +++++++++++Computing trick[{}]++++++++++++++++++++++++'.format(i))
            print('\t trick[{}]={}=1+max of {}'.format(i, trick[i], tem_trick))
            ind_max = np.argmax(tem_trick)
            print('\t index of max value is {}'.format(ind_max))
            if is_trick(ci,cards[ind_max]):
                parent[i] = ind_max
                print('\t ci={}~cards[{}], parent[{}]={}'.format(ci, cards[ind_max], i, ind_max))
            else:
                parent[i] = None
                print('\t ci={}<>{},parent[{}]={}'.format(ci, cards[ind_max], i, None))
    return trick, parent

# 判断两张扑克是否配对
def is_trick(c1, c2):
    if c1[0] == c2[0]:
        return True
    elif c1[1] == c2[1]:
        return True
    elif c1[0] == '8' or c2[0]=='8':
        return True
    else:
        return False

def get_longest_subsequence(cards, trick, parent):
    ind_max = max(trick.keys(), key=(lambda key: trick[key]))
    subsequence = []
    while ind_max is not None:
        subsequence.append(cards[ind_max])
        ind_max = parent[ind_max]
    subsequence.reverse()
    return subsequence

if __name__ == '__main__':
    cards = ['7c', '7h', 'Kc', 'Ks', '8h']
    trick, parent = crazy_eight(cards)
    print( trick)
    sub_cards = get_longest_subsequence(cards, trick, parent)
    print("longest subcards:", sub_cards,'and sum up to', len(sub_cards))
