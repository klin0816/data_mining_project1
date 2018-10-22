import itertools
import ast

min_support = 1

def combination(cList, r):
    combinationSet = [a for a in itertools.combinations(cList, r)]
    return combinationSet

#def combination_new(cList, r):
    


if __name__ == '__main__':
    file = 'data.ntrans_5.tlen_10.nitems_0.02_pre'
    #file = 'file/data'
    full_list = [num for num in range(0, 21)]
    full_dict = {}
    with open(file, 'r') as f:
        mylist = ast.literal_eval(f.read())  # read txt transfer to list
        for n in range(0, 20):
            for sset in combination(full_list, n):
                full_dict[sset] = 0
        for list_length in range(0, len(mylist)):
            for cLength in range(0, len(mylist[list_length])):
                for c_l in combination(mylist[list_length], cLength):
                    nnum = full_dict[c_l]
                    nnum += 1
                    full_dict[c_l] = nnum
        minus_dict = {}
        del full_dict[()]
        for a in full_dict:
            if full_dict[a] > min_support:
                minus_dict[a] = full_dict[a]
        for a in minus_dict:
            print("{}: {}".format(a, minus_dict[a]))
