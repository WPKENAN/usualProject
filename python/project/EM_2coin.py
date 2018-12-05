import scipy.stats
import numpy as np

# 硬币投掷结果观测序列
observations = np.array([[1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                         [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                         [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
                         [1, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                         [0, 1, 1, 1, 0, 1, 1, 1, 0, 1]])

def em_single(observations,priors):
    """
        EM算法的单次迭代
        Arguments
        ------------
        priors:[theta_A,theta_B]
        observation:[m X n matrix]
        Returns
        ---------------
        new_priors:[new_theta_A,new_theta_B]
        :param priors:
        :param observations:
        :return:
    """
    counts = {'A':{'H':0,'T':0},'B':{'H':0,'T':0}};
    theta_A=priors[0];
    theta_B=priors[1];
    for observation in observations:
        len_observation=np.size(observation);
        num_heads=np.sum(observation);
        num_tails=len_observation-np.sum(num_heads);
        contribution_A = scipy.stats.binom.pmf(num_heads,len_observation,theta_A);
        contribution_B = scipy.stats.binom.pmf(num_heads, len_observation, theta_B);
        weight_A=contribution_A/(contribution_A+contribution_B);
        weight_B=contribution_B/(contribution_A+contribution_B);
        counts['A']['H']+=weight_A*num_heads;
        counts['A']['T']+=weight_A*num_tails;
        counts['B']['H']+=weight_B*num_heads;
        counts['B']['T']+=weight_B*num_tails;
    #M step
    new_theta_A=counts['A']['H']/(counts['A']['H']+counts['A']['T']);
    new_theta_B=counts['B']['H']/(counts['B']['H']+counts['B']['T']);
    return [new_theta_A,new_theta_B]

def em(obsevations,prior,tol=1e-5,iterations=1000):
    """
    EM算法
    ：param observations :观测数据
    ：param prior：模型初值
    ：param tol：迭代结束阈值
    ：param iterations：最大迭代次数
    ：return：局部最优的模型参数
    """

    iteration=0;
    while iteration<iterations:
        new_prior=em_single(observations,prior);
        delta_change=np.abs(new_prior[0]-prior[0]);
        if delta_change < tol:
            break
        else:
            prior=new_prior;
            iteration+=1;
        print([iteration,new_prior])

    return [new_prior,iteration]

em(observations, [0.6, 0.5])