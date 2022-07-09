import math, copy

class Fight:

    def __init__(self, room_dims, player_a_pos, player_b_pos, max_dis):

        self.room_x = room_dims[0]
        self.room_y = room_dims[1]

        self.player_a_x = player_a_pos[0]
        self.player_a_y = player_a_pos[1]

        self.player_b_x = player_b_pos[0]
        self.player_b_y = player_b_pos[1]

        self.max_dis = max_dis

        self.max_x = self.player_a_x + self.max_dis + 1
        self.max_y = self.player_a_y + self.max_dis + 1

    def get_dis(self, point_x, point_y):
        dis = math.sqrt((point_x - self.player_a_x) ** 2 + (point_y - self.player_a_y) ** 2)
        return dis

    def get_ang(self, point_x, point_y):
        ang = math.atan2(point_y - self.player_a_y, point_x - self.player_a_x)
        return ang

    def get_q1_mtx(self):

        n_copies_x = math.ceil(self.max_x / self.room_x)
        n_copies_x = int(n_copies_x)
        n_copies_y = math.ceil(self.max_y / self.room_y)
        n_copies_y = int(n_copies_y)

        player_a_exp_x = []
        player_a_exp_y = []
        guard_exp_x = []
        guard_exp_y = []

        for i in range(0, n_copies_x + 1, 1):
            
            temp_player_a_y_list = []
            temp_player_b_y_list = []
            r_x = self.room_x * i

            if len(player_a_exp_x) == 0:
                n_p_p_x = self.player_a_x
            else:
                n_p_p_x = (r_x - player_a_exp_x[-1][0]) + r_x
            player_a_exp_x.append([n_p_p_x, self.player_a_y, 1])

            if len(guard_exp_x) == 0:
                n_g_p_x = self.player_b_x
            else:
                n_g_p_x = (r_x - guard_exp_x[-1][0]) + r_x
            guard_exp_x.append([n_g_p_x, self.player_b_y, 7])

            for j in range(1, n_copies_y + 1, 1):
                r_y = self.room_y * j
                if len(temp_player_b_y_list) == 0:
                    n_g_p_y = (r_y - self.player_b_y) + r_y
                    temp_player_b_y_list.append(n_g_p_y)
                else:
                    n_g_p_y = (r_y - temp_player_b_y_list[-1]) + r_y
                    temp_player_b_y_list.append(n_g_p_y)
                guard_exp_y.append([n_g_p_x, n_g_p_y, 7])

                if len(temp_player_a_y_list) == 0:
                    n_p_p_y = (r_y - self.player_a_y) + r_y
                    temp_player_a_y_list.append(n_p_p_y)
                else:
                    n_p_p_y = (r_y - temp_player_a_y_list[-1]) + r_y
                    temp_player_a_y_list.append(n_p_p_y)
                player_a_exp_y.append([n_p_p_x, n_p_p_y, 1])

        return player_a_exp_x + guard_exp_x + player_a_exp_y + guard_exp_y

    def get_quads(self, q1_mtx):

        q2 = copy.deepcopy(q1_mtx)
        q2t = [-1, 1]
        q2_mtx = []
        for j in range(len(q2)):
            list = [q2[j][i] * q2t[i] for i in range(2)]
            dist = self.get_dis(list[0], list[1])

            if dist <= self.max_dis:
                list.append(q1_mtx[j][2])
                q2_mtx.append(list)

        q3 = copy.deepcopy(q1_mtx)
        q3t = [-1, -1]
        q3_mtx = []
        for j in range(len(q3)):
            list = [q3[j][i] * q3t[i] for i in range(2)]
            dist = self.get_dis(list[0], list[1])

            if dist <= self.max_dis:
                list.append(q1_mtx[j][2])
                q3_mtx.append(list)

        q4 = copy.deepcopy(q1_mtx)
        q4t = [1, -1]
        q4_mtx = []
        for j in range(len(q3)):
            list = [q4[j][i] * q4t[i] for i in range(2)]
            dist = self.get_dis(list[0], list[1])

            if dist <= self.max_dis:
                list.append(q1_mtx[j][2])
                q4_mtx.append(list)

        return q2_mtx, q3_mtx, q4_mtx

    def filter_hits(self, quads_mtx):

        target = {}
        for i in range(len(quads_mtx)):
            dist = self.get_dis(quads_mtx[i][0], quads_mtx[i][1])
            angle = self.get_ang(quads_mtx[i][0], quads_mtx[i][1])
            test_a = self.max_dis >= dist > 0
            test_b = angle not in target
            test_c = angle in target and dist < target[angle][1]
            if test_a and (test_b or test_c):
                target[angle] = [quads_mtx[i], dist]

        return target

    def count_hits(self, hit_points):
        hit_count = 0
        for p in hit_points:
            if hit_points[p][0][2] == 7:
                hit_count += 1
        return hit_count

def solution(room_dims, player_a_pos, player_b_pos, max_dis):

    fight = Fight(room_dims, player_a_pos, player_b_pos, max_dis)

    q1_mtx = fight.get_q1_mtx()

    q2_mtx, q3_mtx, q4_mtx = fight.get_quads(q1_mtx)

    all_q_points = q1_mtx + q2_mtx + q3_mtx + q4_mtx
    hit_points = fight.filter_hits(all_q_points)
    hit_count = fight.count_hits(hit_points)

    return hit_count

room_dims = [3, 2]
player_a_pos = [1, 1]
player_b_pos = [2, 1]
max_dis = 4

result = solution(room_dims, player_a_pos, player_b_pos, max_dis)

# --- additional test cases --- #

# room_dims = [10, 10]
# player_a_pos = [4, 4]
# player_b_pos = [3, 3]
# max_dis = 5000
# result = 739323

# room_dims = [2, 5]
# player_a_pos = [1, 2]
# player_b_pos = [1, 4]
# max_dis = 11
# result 27

# room_dims = [23, 10]
# player_a_pos = [6, 4]
# player_b_pos = [3, 2]
# max_dis = 23
# 0.002 secs and result 8

# room_dims = [300, 275]
# player_a_pos = [150, 150]
# player_b_pos = [180, 100]
# max_dis = 500
# 0.65 secs and result 9

# room_dims = [3, 2]
# player_a_pos = [1, 1]
# player_b_pos = [2, 1]
# max_dis = 4
# 0 secs and result 7

# room_dims = [1250, 1250]
# player_a_pos = [1000, 1000]
# player_b_pos = [500, 400]
# max_dis = 10000
# 204 sec and result of 196
# v0.2 183 secs and result of 196
