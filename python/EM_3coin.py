import numpy as np
from scipy import stats

def em_single(priors, observations):
    """
    EM算法单次迭代
    Arguments
    ---------
    priors : [theta_A, theta_B，theta_C]
    observations : [m X n matrix]

    Returns
    --------
    new_priors: [new_theta_A, new_theta_B,new_theta_C]
    :param priors:
    :param observations:
    :return:
    """
    counts = {'A': {'H': 0, 'T': 0}, 'B': {'H': 0, 'T': 0}}
    theta_A = priors[0]
    theta_B = priors[1]
    theta_c=priors[2]
    # E step
    weight_As=[]
    for observation in observations:
        len_observation = len(observation)
        num_heads = observation.sum()
        num_tails = len_observation - num_heads
        contribution_A = theta_c*stats.binom.pmf(num_heads, len_observation, theta_A)
        contribution_B = (1-theta_c)*stats.binom.pmf(num_heads, len_observation, theta_B)  # 两个二项分布
        weight_A = contribution_A / (contribution_A + contribution_B)
        weight_B = contribution_B / (contribution_A + contribution_B)
        # 更新在当前参数下A、B硬币产生的正反面次数
        weight_As.append(weight_A)
        counts['A']['H'] += weight_A * num_heads
        counts['A']['T'] += weight_A * num_tails
        counts['B']['H'] += weight_B * num_heads
        counts['B']['T'] += weight_B * num_tails

    # M step
    new_theta_c = 1.0*sum(weight_As)/len(weight_As)
    new_theta_A = counts['A']['H'] / (counts['A']['H'] + counts['A']['T'])
    new_theta_B = counts['B']['H'] / (counts['B']['H'] + counts['B']['T'])
    return [new_theta_A, new_theta_B,new_theta_c]

def em(observations, prior, tol=1e-6, iterations=10000):
    """
    EM算法
    :param observations: 观测数据
    :param prior: 模型初值
    :param tol: 迭代结束阈值
    :param iterations: 最大迭代次数
    :return: 局部最优的模型参数
    """
    import math
    iteration = 0
    while iteration < iterations:
        new_prior = em_single(prior, observations)
        delta_change = np.abs(prior[0] - new_prior[0])
        if delta_change < tol:
            break
        else:
            prior = new_prior
            iteration += 1
    return [new_prior, iteration]

# 硬币投掷结果观测序列：1表示正面，0表示反面。
observations = np.array([[1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                         [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
                         [1, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                         [0, 1, 1, 1, 0, 1, 1, 1, 0, 1]])

print(em(observations, [0.5, 0.8, 0.6]))