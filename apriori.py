import itertools
import ast
import pprint
import sys


def support(min_support_rate, total_transcation):
    return float(min_support_rate) * float(total_transcation)

def combination(cList, r):
    combinationSet = [a for a in itertools.combinations(cList, r)]
    return combinationSet

if __name__ == '__main__':
    if(sys.argv[1]):
        file = sys.argv[1]
    else:
        file = 'dataset/data_test'
    if(sys.argv[2]):
        min_support_rate = sys.argv[2]
    else:
        min_support_rate = 0.5
    if(sys.argv[3]):
        min_confidence = float(sys.argv[3])
    else:
        min_confidence = 0.5
    with open(file, 'r') as f:
        mylist = ast.literal_eval(f.read())  # read txt transfer to list
        r = 1
        transcation_num = 0
        list_last = [] 
        minus, support_confidence, full_dict = ({} for i in range(3))
        full_list = []    # get every exist element
        for aa in mylist:
            transcation_num += 1
            for bb in aa:
                if bb not in full_list:
                    full_list.append(bb)
        full_list.sort()
        min_support = support(min_support_rate, transcation_num)
        list_sset = [list(sset) for sset in combination(full_list, 1)]
        list_sset_len = len(list_sset)
        for sset in combination(full_list, 1):
            full_dict[sset] = 0
        for r in range(1, list_sset_len+1):
            for list_length in range(0, len(mylist)):   # for every transcation
                if r <= len(mylist[list_length]):   # nCr, r<=n
                    for cresult in combination(mylist[list_length], r):
                        if cresult in full_dict:
                            nnum = full_dict[cresult]   # full dict ++
                            nnum += 1
                            full_dict[cresult] = nnum
            for element in full_dict:   # should > min_support
                if full_dict[element] > min_support:
                    minus[element] = full_dict[element]
                    list_last.append(element)
                    for i in range(0, full_dict[element]):
                        if len(list(element)) == r:
                            list_element = list(element)
                            for r2 in range(1, len(list_element)):
                                for ccc in combination(list_element, r2):
                                    ddd = set(list_element[:])
                                    cc = set(ccc)
                                    if set(ccc).issubset(ddd):
                                        ddd = ddd - cc
                                        stt = str(cc) + '->' + str(ddd)
                                        if stt not in support_confidence:
                                            support_confidence[stt] = {'#SUP':1}
                                        else:
                                            support_confidence[stt]['#SUP'] += 1
                                        support_confidence[stt]['#CONF'] = float(support_confidence[stt]['#SUP'] / full_dict[ccc])
            full_dict = minus   
            list_combination = []
            for tu in list_last:    # find left element
                for num in tu:
                    if num not in list_combination:
                        list_combination.append(num)
            list_combination.sort()
            for sset in combination(list_combination, r+1): 
                # use left element do combination
                full_dict[sset] = 0
            minus = {}
        for key in list(support_confidence.keys()):
            if support_confidence[key]['#CONF'] < min_confidence:
                del support_confidence[key]
            
        pprint.pprint(support_confidence)
        
        # list_last: element of last
        # full_dict: dict of element and count
