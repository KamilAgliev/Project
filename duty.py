from collections import deque


class Duty:
    def __init__(self, name, people, gr):
        self.name = name
        self.people = people
        self.people.sort()
        self.gr = int(gr)
        self.bad = deque()
        self.q = deque()
        for i in range(len(people)):
            self.q.append(people[i])

    def left(self, people):
        for p in people:
            try:
                self.bad.append(p)
                self.q.remove(p)
            except RuntimeError:
                pass

    def returned(self, people):
        for p in people:
            try:
                self.bad.remove(p)
                self.q.appendleft(p)
            except RuntimeError:
                pass

    def duty_now(self):
        on_duty = []
        for i in range(min(len(self.q), self.gr)):
            cur_man = self.q.popleft()
            on_duty.append(cur_man)
            self.q.append(cur_man)
        return on_duty


