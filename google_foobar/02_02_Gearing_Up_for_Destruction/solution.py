from fractions import Fraction

def get_specs(pegs):

    n_pegs = len(pegs)

    is_even = False

    if n_pegs%2 == 0:
        is_even = True

    if is_even:
        pegs_sum = (-pegs[0]+pegs[n_pegs-1])
    else:
        pegs_sum = (- pegs[0] - pegs[n_pegs -1])

    return n_pegs, is_even, pegs_sum

def solution(pegs):

    n_pegs, is_even, pegs_sum = get_specs(pegs)

    if ((not pegs) or n_pegs == 1):
        return [-1,-1]

    if (n_pegs > 2):
        for idx in xrange(1, n_pegs-1):
            pegs_sum += 2 * (-1)**(idx+1) * pegs[idx]

    if is_even:
        fg_rad = Fraction(2 * float(pegs_sum) / 3).limit_denominator()
    else:
        fg_rad = Fraction(2 * pegs_sum).limit_denominator()

    # -- break on fg_rad < 2 which makes lg_rad < 1 -- #

    if fg_rad < 2:
        return [-1,-1]

    cur_rad = fg_rad

    # --- loop pegs --- #
    for idx in range(0, n_pegs-2):
        
        cent_dist = pegs[idx+1] - pegs[idx]
        next_rad = cent_dist - cur_rad
        
        if (cur_rad < 1 or next_rad < 1):
            return [-1,-1]
        else:
            cur_rad = next_rad

    return [fg_rad.numerator, fg_rad.denominator]

test_1 = [4,30,50]
test_2 = [4,17,50]

result = solution(test_1)


