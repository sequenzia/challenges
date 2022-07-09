from collections import defaultdict

def gen_bit_map(a_val,b_val,bit_len):
    a_bit_val = a_val & ~(1<<bit_len)
    b_bit_val = b_val & ~(1<<bit_len)
    c_bit_val = a_val >> 1
    d_bit_val = b_val >> 1

    return (a_bit_val&~b_bit_val&~c_bit_val&~d_bit_val) | \
           (~a_bit_val&b_bit_val&~c_bit_val&~d_bit_val) | \
           (~a_bit_val&~b_bit_val&c_bit_val&~d_bit_val) | \
           (~a_bit_val&~b_bit_val&~c_bit_val&d_bit_val)

def build_map(n, g_nums):
    g_map = defaultdict(set)
    g_set = set(g_nums)

    for i in range(1<<(n+1)):
        for j in range(1<<(n+1)):
            bit_map = gen_bit_map(i,j,n)
            if bit_map in g_nums:
                g_map[(bit_map, i)].add(j)
    return g_map

def solution(g):
    g = list(zip(*g))
    n_rows = len(g)
    n_cols = len(g[0])

    g_nums = [sum([1<<i if col else 0 for i, col in enumerate(row)]) for row in g]
    g_map = build_map(n_cols, g_nums)

    pre_img = {i: 1 for i in range(1<<(n_cols+1))}

    for row in g_nums:
        next_row = defaultdict(int)
        for c1 in pre_img:
            for c2 in g_map[(row, c1)]:
                next_row[c2] += pre_img[c1]
        pre_img = next_row

    return sum(pre_img.values())

test_1 = [[True,False,True],
          [False,True,False],
          [True,False,True]]

test_2 = [[True, True, False, True, False, True, False, True, True, False],
          [True, True, False, False, False, False, True, True, True, False],
          [True, True, False, False, False, False, False, False, False, True],
          [False, True, False, False, False, False, True, True, False, False]]

result = solution(test_1)





