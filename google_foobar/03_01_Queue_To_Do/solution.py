from functools import reduce
from operator import xor

def sub_base_fn(n):
    n_div = n%4
    if n_div == 0:
        return n
    if n_div == 1:
        return 1
    if n_div == 2:
        return n+1
    if n_div == 3:
        return 0

def sub_rngs_fn(st_id, wrks_len):

    rng_ed = wrks_len+st_id+1

    rngs = []

    idx = 0
    for n in xrange(st_id,rng_ed):
        f = st_id  + (idx * wrks_len)
        g = f + wrks_len - idx - 1

        if idx < wrks_len:
            rngs.insert(idx,[f,g])

        idx+=1
    return rngs

def solution(st_id, wrks_len):

    if wrks_len == 1:
        return st_id

    if wrks_len == 2:
        a = st_id
        b = st_id + 1
        c = st_id + 2
        return xor(xor(a, b), c)

    if wrks_len > 2:

        sub_rngs = sub_rngs_fn(st_id,wrks_len)

        rng_log = []
        z_log = []

        is_last_idx = False

        chksum_res = 0

        for idx, sub_rng in enumerate(sub_rngs):

            if idx == len(sub_rngs)-1:
                is_last_idx = True

            rng_a = max(sub_rng[0]-1,0)
            rng_b = sub_rng[-1]

            if idx == len(sub_rngs)-1:
                rng_xor = rng_b
            else:
                sub_a = sub_base_fn(rng_a)
                sub_b = sub_base_fn(rng_b)
                rng_xor = xor(sub_b, sub_a)

            rng_log.append(rng_xor)

        for idx in range(len(rng_log)):

            if idx == 1:
                z_st = rng_log[idx-1]

            if idx > 1:
                z_st = z_log[-1]

            if idx > 0:
                z_ed = rng_log[idx]
                z = xor(z_st,z_ed)
                z_log.append(z)

                if idx == len(rng_log) - 1:
                    chksum_res = z

        return chksum_res

test_1 = (0,3)
test_2 = (17,4)

result = solution(*test_1)

