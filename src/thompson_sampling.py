import random

class ThompsonSampling:
    def __init__(self, n_ads):
        self.n_ads = n_ads
        self.numbers_of_rewards_1 = [1] * n_ads 
        self.numbers_of_rewards_0 = [1] * n_ads  

    def select_ad(self):
        ad = 0
        max_random = 0
        for i in range(self.n_ads):
            random_beta = random.betavariate(self.numbers_of_rewards_1[i], self.numbers_of_rewards_0[i])
            if random_beta > max_random:
                max_random = random_beta
                ad = i
        return ad

    def update(self, ad, reward):
        if reward == 1:
            self.numbers_of_rewards_1[ad] += 1
        else:
            self.numbers_of_rewards_0[ad] += 1
