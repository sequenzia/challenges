from fractions import Fraction

# -- mtx specs func -- #
def mtx_specs_fn(mtx):

    mtx_len = len(mtx)

    term_states = []
    non_term_states = []

    probs_mtx = mtx[:]

    # Get term and non-term states
    for row_idx in range(mtx_len):

        count = 0
        probs_total = 0

        for val_idx in range(len(probs_mtx[row_idx])):

            # -- update count -- #
            if probs_mtx[row_idx][val_idx] == 0:
                count += 1

            # -- update probs -- #
            probs_total += probs_mtx[row_idx][val_idx]

        if probs_total != 0:
            for val_idx in range(len(probs_mtx[row_idx])):
                probs_mtx[row_idx][val_idx] /= float(probs_total)

        # -- set term states -- #
        if count == mtx_len:
            term_states.append(row_idx)
        else:
            non_term_states.append(row_idx)

    return term_states, non_term_states, probs_mtx

# -- RQ func -- #
def rq_fn(probs_mtx, term_states, non_term_states):
    '''
    R - non-terminal -> terminal
    Q - non-terminal -> non-terminal
    '''
    R = []
    Q = []
    for i in non_term_states:
        temp_t = []
        temp_n = []
        for j in term_states:
            temp_t.append(probs_mtx[i][j])
        for j in non_term_states:
            temp_n.append(probs_mtx[i][j])
        R.append(temp_t)
        Q.append(temp_n)
    return R, Q

# -- identity matrix - Q -- #
def ident_sub_q_fn(Q):
    n = len(Q)
    for row in range(len(Q)):
        for item in range(len(Q[row])):
            if row == item:
                Q[row][item] = 1 - Q[row][item]
            else:
                Q[row][item] = -Q[row][item]
    return Q

# -- minor matrix -- #
def minor_mtx_fn(Q, i, j):
    minor_matrix = []
    for row in Q[:i] + Q[i + 1:]:
        temp = []
        for item in row[:j] + row[j + 1:]:
            temp.append(item)
        minor_matrix.append(temp)
    return minor_matrix

# -- determinant of a square matrix -- #
def determinant_fn(Q):
    if len(Q) == 1:
        return Q[0][0]
    if len(Q) == 2:
        return Q[0][0] * Q[1][1] - Q[0][1] * Q[1][0]

    determinant = 0
    for first_row_item in range(len(Q[0])):
        minor_matrix = minor_mtx_fn(Q, 0, first_row_item)
        determinant += (((-1) ** first_row_item) * Q[0][first_row_item] * determinant_fn(minor_matrix))

    return determinant

# -- transpose of a square matrix -- #
def trans_sq_mtx_fn(Q):
    for i in range(len(Q)):
        for j in range(i, len(Q), 1):
            Q[i][j], Q[j][i] = Q[j][i], Q[i][j]
    return Q

# -- inverse func -- #
def inverse_fn(Q):
    Q1 = []
    for row_idx in range(len(Q)):
        temp = []
        for col_idx in range(len(Q[row_idx])):
            minor_matrix = minor_mtx_fn(Q, row_idx, col_idx)
            determinant = determinant_fn(minor_matrix)
            temp.append(((-1) ** (row_idx + col_idx)) * determinant)
        Q1.append(temp)
    main_determinant = determinant_fn(Q)
    Q1 = trans_sq_mtx_fn(Q1)
    for i in range(len(Q)):
        for j in range(len(Q[i])):
            Q1[i][j] /= float(main_determinant)
    return Q1

# -- multiply matrix func -- #
def multiply_mtx_fn(A, B):
    result = []
    dimension = len(A)
    for row_idx in range(len(A)):
        temp = []
        for col_idx in range(len(B[0])):
            product = 0
            for selector in range(dimension):
                product += (A[row_idx][selector] * B[selector][col_idx])
            temp.append(product)
        result.append(temp)
    return result

# -- gcd func -- #
def gcd_fn(a, b):
    if b == 0:
        return a
    else:
        return gcd_fn(b, a % b)

# -- sanitize func -- #
def sanitize_fn(M):
    M_0 = M[0]
    to_fraction = [Fraction(i).limit_denominator() for i in M_0]
    lcm = 1
    for i in to_fraction:
        if i.denominator != 1:
            lcm = i.denominator
    for i in to_fraction:
        if i.denominator != 1:
            lcm = lcm * i.denominator / gcd_fn(lcm, i.denominator)
    to_fraction = [(i * lcm).numerator for i in to_fraction]
    to_fraction.append(lcm)
    return to_fraction

def solution(mtx):

    if len(mtx) == 1:
        if len(mtx[0]) == 1 and mtx[0][0] == 0:
            return [1, 1]

    term_states, non_term_states, probs_mtx = mtx_specs_fn(mtx)

    # Get R and Q matrix
    R, Q = rq_fn(probs_mtx, term_states, non_term_states)
    IQ = ident_sub_q_fn(Q)

    # Get Fundamental Matrix (F)
    IQ1 = inverse_fn(IQ)

    product_IQ1_R = multiply_mtx_fn(IQ1, R)

    return sanitize_fn(product_IQ1_R)

test_1 = [[0, 2, 1, 0, 0],
          [0, 0, 0, 3, 4],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]

test_2 = [[0, 1, 0, 0, 0, 1],
          [4, 0, 0, 3, 2, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]

result = solution(test_1)


