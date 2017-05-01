import sys,random, math, operator
from operator import itemgetter


random.seed(0)


class UserBasedCF:
    def __init__(self):
        self.trainset = {}
        self.testset = {}
        self.resultset = {}
        self.mean = {}

        self.user_max = 0
        self.item_max = 0

        self.sim_vector = {}
        self.sim_rank = {}
        self.mse = 0.0

    @staticmethod
    def loadfile(filename):
        fp = open(filename, 'r')
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
        fp.close()

    def generate_dataset(self, filename, pivot=0.7):
        trainset_len = 0
        testset_len = 0

        for line in UserBasedCF.loadfile(filename):
            user, movie, rating, timestamp = line.split('\t')
            user = int(user)
            movie = int(movie)
            rating = int(rating)
            self.user_max = max(self.user_max, user)
            self.item_max = max(self.item_max, movie)
            self.trainset.setdefault(user, {})
            self.testset.setdefault(user, {})
            if random.random() < pivot:
                self.trainset[user][movie] = rating
                trainset_len += 1
            else:
                self.testset[user][movie] = rating
                testset_len += 1

        for user in range(1, self.user_max+1):
            all = 0.0
            num = 0
            for item in range(1, self.item_max+1):
                if item in self.trainset[user]:
                    all += self.trainset[user][item]
                    num += 1
            self.mean[user] = all / num

        print testset_len

    def cal_user_sim(self):
        self.sim_vector.clear()

        for u1 in range(1, self.user_max+1):
            self.sim_vector.setdefault(u1, {})
            # if u1 % 100 == 0:
            #     print u1
            for u2 in range(u1+1, self.user_max+1):
                self.sim_vector.setdefault(u2, {})
                xy = 0.0
                xx = 0.0
                yy = 0.0
                if u1 in self.trainset and u2 in self.trainset:
                    for index in range(1, self.item_max+1):
                        if index in self.trainset[u1] and index in self.trainset[u2]:
                            xy += self.trainset[u1][index] * self.trainset[u2][index]
                            xx += self.trainset[u1][index] * self.trainset[u1][index]
                            yy += self.trainset[u2][index] * self.trainset[u2][index]
                    if math.sqrt(xx)*math.sqrt(yy) > 0:
                        self.sim_vector[u1][u2] = xy / (math.sqrt(xx)*math.sqrt(yy))
                        self.sim_vector[u2][u1] = self.sim_vector[u1][u2]
                    else:
                        self.sim_vector[u1][u2] = 0
                        self.sim_vector[u2][u1] = self.sim_vector[u1][u2]

    def cal_user_sim2(self):
        self.sim_vector.clear()
        for u1 in range(1, self.user_max+1):
            self.sim_vector.setdefault(u1, {})
            # if u1 % 100 == 0:
            #     print u1
            for u2 in range(u1+1, self.user_max+1):
                self.sim_vector.setdefault(u2, {})
                xy = 0.0
                xx = 0.0
                yy = 0.0
                num_both = 0.0
                num1 = 0.0
                num2 = 0.0
                if u1 in self.trainset and u2 in self.trainset:
                    for i in range(1, self.item_max+1):
                        if i in self.trainset[u1]:
                            num1 += 1
                        if i in self.trainset[u2]:
                            num2 += 1
                        if i in self.trainset[u1] and i in self.trainset[u2]:
                            num_both += 1
                            xy += self.trainset[u1][i] * self.trainset[u2][i]
                            xx += self.trainset[u1][i] * self.trainset[u1][i]
                            yy += self.trainset[u2][i] * self.trainset[u2][i]

                    if math.sqrt(xx) * math.sqrt(yy) > 0:
                        self.sim_vector[u1][u2] = xy / (math.sqrt(xx)*math.sqrt(yy)) * num_both * num_both / num1 / num2
                        self.sim_vector[u2][u1] = self.sim_vector[u1][u2]
                    else:
                        self.sim_vector[u1][u2] = 0
                        self.sim_vector[u2][u1] = self.sim_vector[u1][u2]

    def getRecommendation(self, k):
        self.sim_rank.clear()
        self.resultset.clear()
        for i in range(1, self.user_max+1):
            self.sim_rank.setdefault(1, {})
            self.sim_rank[i] = sorted(self.sim_vector[i].iteritems(), key=lambda x: x[1], reverse=True)
        for i in range(1, self.user_max+1):
            self.resultset.setdefault(i, {})
            for j in range(1, self.item_max+1):
                sim_sum = 0.0
                if j not in self.trainset[i]:
                    self.resultset[i][j] = 0.0
                    for kk in range(0, k):
                        sim_user = self.sim_rank[i][kk][0]
                        sim_value = self.sim_rank[i][kk][1]
                        if j in self.trainset[sim_user]:
                            self.resultset[i][j] += (self.trainset[sim_user][j] - self.mean[sim_user]) * sim_value
                        sim_sum += sim_value
                    self.resultset[i][j] /= sim_sum
                    self.resultset[i][j] += self.mean[i]
                    if self.resultset[i][j] < 0:
                        self.resultset[i][j] = 0

    def evaluation(self):
        mse_cnt = 0
        self.mse = 0.0
        for i in range(1, self.user_max+1):
            for j in range(1, self.item_max+1):
                if j in self.testset[i]:
                    self.mse += (self.testset[i][j] - self.resultset[i][j]) * (self.testset[i][j] - self.resultset[i][j])
                    mse_cnt += 1
        self.mse /= mse_cnt

if __name__ == '__main__':
    usercf = UserBasedCF()
    usercf.generate_dataset('u.data')

    for i in range(5, 35, 5):
        print '---------------------------------------'
        usercf.cal_user_sim()
        usercf.getRecommendation(i)
        usercf.evaluation()
        print i, usercf.mse

        usercf.cal_user_sim2()
        usercf.getRecommendation(i)
        usercf.evaluation()
        print i, usercf.mse



