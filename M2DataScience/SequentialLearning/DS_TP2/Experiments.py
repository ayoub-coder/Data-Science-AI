import numpy as np
from matplotlib import pyplot as plt

def OneBanditOneLearnerOneRun(bandit, strategy, timeHorizon):
    """
    Run a bandit strategy (strategy) on a MAB instance (bandit) for (timeHorizon) time steps
    output : sequence of arms chosen, sequence of rewards obtained
    """
    selections = []
    rewards = []
    strategy.clear() # reset previous history
    for t in range(timeHorizon):
        # choose the next arm to play with the bandit algorithm
        arm = strategy.chooseArmToPlay()
        # get the reward of the chosen arm
        reward = bandit.generateReward(arm)
        # update the algorithm with the observed reward
        strategy.receiveReward(arm, reward)
        # store what happened
        selections.append(arm)
        rewards.append(reward)
    return selections, rewards

def CumulativeRegret(bandit,selections):
    """Compute the pseudo-regret associated to a sequence of arm selections"""
    return np.cumsum(max(bandit.means)*np.ones(len(selections)) - np.array(bandit.means)[selections])

def OneBanditOneLearnerMultipleRuns(bandit, strategy, timeHorizon, N_exp, tsave=[]):
    """
    Perform N_exp runs of a bandit strategy (strategy) on a MAB instance (bandit) for (timeHorizon) time steps 
    and compute the pseudo-regret of each run 
    optional : tsave gives a grid of time steps in which the results will be stored (set to 1:timeHorizon by default)
    output : a table of size N_exp x |tsave| in which each row is the pseudo-regret at the sub-sampled times 
    """
    if (len(tsave) == 0):
        tsave = np.arange(timeHorizon)
    savedTimes = len(tsave)
    Regret = np.zeros((N_exp, savedTimes)) # Store the regret values on different runs
    for n in range(N_exp):
        np.random.seed()
        # run the bandit strategy
        selections, rewards = OneBanditOneLearnerOneRun(bandit, strategy, timeHorizon)
        # compute its pseudo-regret
        regret_one_run = CumulativeRegret(bandit, selections)
        # store (a sub-sampling of) the cumulative regret
        Regret[n, :] = np.array(regret_one_run)[tsave] 
    return Regret

def RunExpes(algorithms,bandit,N_exp,timeHorizon,step=10,quantiles = "on",names=[]):
    """run experiments with multiple algorithms"""
    plt.clf()
    tsave = np.arange(1,timeHorizon,step)
    colors = ["b","r","g","k","m"]
    if (names==[]):
        names = [algo.name() for algo in algorithms]
    for i in range(len(algorithms)):
        algo=algorithms[i]
        Regret = OneBanditOneLearnerMultipleRuns(bandit, algo, timeHorizon, N_exp, tsave)
        plt.plot(tsave, np.mean(Regret, 0), linewidth=2.0, color=colors[i], label="mean regret of "+ names[i])
        if (quantiles == "on"):
            plt.plot(tsave, np.quantile(Regret, 0.95, 0), tsave, np.quantile(Regret,0.05,0), linestyle="dashed", color=colors[i])
    plt.legend()
    plt.show()


def ViewSelections(selections):
    plt.clf()
    nbBins=max(selections) + 1
    plt.xlabel("Arms", fontsize=14)
    plt.ylabel("Number of arms selections", fontsize=14)
    plt.hist(selections, nbBins)
    plt.title("Number of selections of each arm", fontsize=14)
    axes=plt.gca()
    axes.xaxis.set_ticks(range(nbBins))
