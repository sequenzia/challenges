SPLIT_ODD = False
SPLIT_EVEN = False
SPLIT_ALTS = False
STOP_EARLY = True
LOG_ON = False

class Fuel():

    def __init__(self):

        self.branches = []
        self.steps_queue = []

        self.min_branch = None
        self.min_count = 999999

    def add_branch(self,
                   pos,
                   dest,
                   step_count=0,
                   parent=None):

        if parent is None:
            _branch = Branch(self,pos,dest,step_count,parent)
            self.branches.append(_branch)
            return _branch

        if parent is not None:

            if parent.steps_count + step_count < self.min_count:

                child_step_count = parent.steps_count + step_count

                _branch = Branch(self,pos,dest,child_step_count,parent)

                if LOG_ON:
                    _branch.steps_log.append(parent.steps_log.copy())

                self.branches.append(_branch)

                return _branch

            else:

                return

    def load(self,
             pos,
             dest):

        branch = self.add_branch(pos,dest)

        branch.run_fuel(pos, dest)

        while len(self.steps_queue) > 0:
            self.run_queue()

    def run_queue(self):

        _queue = self.steps_queue.copy()

        if len(_queue) > 0:

            for q in _queue:

                branch = q[0]
                pos = q[1]
                dest = q[2]

                if branch.is_active:
                    branch.run_fuel(pos,dest)

                self.steps_queue.remove(q)

class Branch():

    def __init__(self,
                 fuel,
                 pos,
                 dest,
                 step_count=0,
                 parent=None):

        self.fuel = fuel

        self.pos = pos
        self.dest = dest
        self.parent_branch = parent

        self.is_pri = False

        if self.parent_branch is None:
            self.is_pri = True

        self.sub_branches = []

        self.steps_log = []

        self.steps_count = step_count

        self.dest_hit = False
        self.is_active = True

    def add_log(self,
                step_type,
                dest,
                in_pos,
                out_pos):

        _log = {'type': step_type,
                'dest': dest,
                'in_pos': in_pos,
                'out_pos': out_pos,
                'count': self.steps_count}

        self.steps_log.append(_log)

    def is_even(self,
                pos):
        return pos % 2 == 0

    def is_odd(self,
               pos):
        return pos % 2 != 0

    def cur_dist(self,
                 pos,
                 dest):
        return int(pos-dest)

    def stop_chk(self):

        if STOP_EARLY:
            if self.steps_count >= self.fuel.min_count:
                self.is_active = False

    def flag_hit(self):

        self.dest_hit = True
        self.is_active = False

        if self.steps_count < self.fuel.min_count:
            self.fuel.min_count = self.steps_count
            self.fuel.min_branch = self

    def step(self,
             pos,
             dest):

        out_pos = pos-1

        self.steps_count += 1

        if LOG_ON:
            self.add_log('single_step',dest,pos,out_pos)

        if out_pos == dest:
            self.dest_hit = True
            self.is_active = False

        return out_pos

    def half_step(self,
                  pos,
                  dest):

        if self.is_odd(pos):
            return 'odd_half'

        out_pos = int(pos // 2)

        self.steps_count += 1

        if LOG_ON:
            self.add_log('half_step',dest,pos,out_pos)

        if out_pos == dest:
            self.dest_hit = True
            self.is_active = False

        return out_pos

    def action_fn(self,
                  pos,
                  dest):

        if self.is_active:

            if self.cur_dist(pos,dest) == 0:
                self.flag_hit()
                return 0

            if pos <= 3:

                if pos == 3:
                    pri_pos = self.step(pos,dest)
                    pri_pos = self.step(pri_pos,dest)
                    self.flag_hit()
                    return 0

                if pos == 2:
                    pri_pos = self.step(pos,dest)
                    self.flag_hit()
                    return 0
            else:

                if self.is_even(pos):

                    pri_pos = pos

                    if SPLIT_EVEN:

                        if self.is_pri or SPLIT_ALTS:

                            pos_m2 = pos-2
                            pos_p2 = pos+2

                            alt_a_branch = self.fuel.add_branch(pos_m2,dest,2,self)
                            alt_b_branch = self.fuel.add_branch(pos_p2,dest,2,self)

                            if alt_a_branch is not None:

                                self.sub_branches.append(alt_a_branch)

                                if LOG_ON:
                                    alt_a_branch.add_log('even_split',dest,pos,pos_m2)

                                self.fuel.steps_queue.append([alt_a_branch,pos_m2,dest])

                            if alt_b_branch is not None:

                                self.sub_branches.append(alt_b_branch)

                                if LOG_ON:
                                    alt_b_branch.add_log('even_split',dest,pos,pos_p2)

                                self.fuel.steps_queue.append([alt_b_branch,pos_p2,dest])

                if self.is_odd(pos):

                    pos_m1 = pos-1
                    pos_p1 = pos+1

                    if self.is_even(pos_m1 // 2):
                        pri_pos = pos_m1
                        alt_pos = pos_p1
                    else:
                        pri_pos = pos_p1
                        alt_pos = pos_m1

                    self.steps_count += 1

                    if LOG_ON:
                        self.add_log('pri_odd_split',dest,pos,pri_pos)

                    if SPLIT_ODD:

                        if self.is_pri or SPLIT_ALTS:

                            alt_branch = self.fuel.add_branch(alt_pos,dest,1,self)

                            if alt_branch is not None:

                                self.sub_branches.append(alt_branch)

                                if LOG_ON:
                                    alt_branch.add_log('alt_odd_split',dest,pos,alt_pos)

                                self.fuel.steps_queue.append([alt_branch,alt_pos,dest])

            return pri_pos

        return

    def run_fuel(self,
                 pos,
                 dest):

        while self.is_active:
            self.stop_chk()
            pos = self.action_fn(pos,dest)

            if self.is_active:
                self.stop_chk()
                pos = self.half_step(pos,dest)

def solution(pos):

    pos = int(pos)

    if pos == 0:
        return 0

    if pos <= 3 and pos > 0:
        return pos-1

    fuel = Fuel()
    fuel.load(pos,1)

    return fuel.min_count

test_1 = '15'
test_2 = '4'

result = solution(test_1)
