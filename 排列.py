import itertools
from copy import deepcopy
def swap(li, i, j):
    if i == j:
        return
    temp = li[j]
    li[j] = li[i]
    li[i] = temp


def reverse(li, i, j):
    """
    翻转
    :param li: 字符串数组
    :param i: 翻转开始位置
    :param j: 翻转结束位置
    """
    if li is None or i < 0 or j < 0 or i >= j or len(li) < j + 1:
        return
    while i < j:
        swap(li, i, j)
        i += 1
        j -= 1


def get_next_permutation(li, size):
    # 后找：字符串中最后一个升序的位置i，即：S[i]<S[i+1]
    i = size - 2
    while i >= 0 and li[i] >= li[i + 1]:
        i -= 1
    if i < 0:
        return False
    # 查找(小大)：S[i+1…N-1]中比S[i]大的最小值S[j]
    j = size - 1
    while li[j] <= li[i]:
        j -= 1
    # 交换：S[i]，S[j]
    swap(li, i, j)
    # 翻转：S[i+1…N-1]
    reverse(li, i + 1, size - 1)
    return True


if __name__ == '__main__':
    li = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    li.sort()  # 初始的li必须是正序的 [1, 2, 2, 3, 4, 5]
    size = len(li)
    result = [deepcopy(li)]
    while get_next_permutation(li, size):
        result.append(deepcopy(li))
    for i in result:
        #前面4位后面5位
        if (i[0]*10+i[1])*(i[2]*10+i[3])==i[4]*(i[5]*1000+i[6]*100+i[7]*10+i[8]):   #2*2 1*4
            print((i[0]*10+i[1]),(i[2]*10+i[3]),i[4],(i[5]*1000+i[6]*100+i[7]*10+i[8]),(i[0]*10+i[1])*(i[2]*10+i[3]))
        if (i[0]*10+i[1])*(i[2]*10+i[3])==(i[4]*10+i[5])*(i[6]*100+i[7]*10+i[8]):   #2*2 2*3
            print((i[0]*10+i[1]),(i[2]*10+i[3]),i[4]*10+i[5],(i[6]*100+i[7]*10+i[8]),(i[0]*10+i[1])*(i[2]*10+i[3]))
        if i[0]*(i[1]*100+i[2]*10+i[3])==(i[4]*10+i[5])*(i[6]*100+i[7]*10+i[8]):
            print((i[0]*10+i[1]),(i[2]*10+i[3]),i[4]*10+i[5],(i[6]*100+i[7]*10+i[8]),i[0]*(i[1]*100+i[2]*10+i[3]))
        if i[0]*(i[1]*100+i[2]*10+i[3])==i[4]*(i[5]*1000+i[6]*100+i[7]*10+i[8]):
            print((i[0]),(i[1]*100+i[2]*10+i[3]),i[4],(i[5]*1000+i[6]*100+i[7]*10+i[8]),i[0]*(i[1]*100+i[2]*10+i[3]))
        
    print("OK")


