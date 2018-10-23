import pickle
import sys

if __name__ == '__main__':
    file = sys.argv[1]
    big_list = []
    with open(file, "r") as f:
        temp = []
        start = 1
        sstring = ''
        for line in f:
            s = line.rsplit()
            if int(s[1]) > start:
                start += 1
                big_list.append(temp)
                temp = []
                sstring += '\n'
            else:
                temp.append(int(s[2]))
                sstring = sstring + str(s[2]) + ' '
        #print("{}".format(s[2]))
        #print(big_list)

    with open(file + "_pre", "w") as fp:
        fp.write(str(big_list))

    with open(file + "_p", "w") as ft:
        ft.write(str(sstring))
    
    print("Proceed!")
