# -*- coding: utf-8 -*-
from agent import *
import numpy as np
import os
import imageio.v2 as imageio
import argparse
import warnings

warnings.filterwarnings("ignore")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run simulation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--num_simulations",
        default=30,
        type=int,
        help="number of simulations to run",
    )
    parser.add_argument(
        "--agents",
        default=0,
        type=int,
        nargs="+",
        help="list of agents to run, should input numbers from 0 to 7",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print out the steps of each simulation",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="visualize the simulation with a video",
    )
    return parser.parse_args()


class Simulation(object):
    def __init__(self, num_simulations: int = 30, squad: list = [GraphAgent0]) -> None:
        self.num_simulations = num_simulations
        self.squad = squad
        self.results = {}
        for Agent in squad:
            self.results[Agent.__name__] = []

    def run(self, verbose: bool = False, visualize: bool = False):
        for i in range(self.num_simulations):
            if verbose:
                print("============== Simulation {} ==============".format(i + 1))

            # start the game
            for Agent in self.squad:
                if verbose:
                    print("============== {} ==============".format(Agent.__name__))
                agent = Agent()
                agent.initialize()
                num_steps = 0
                print(agent.agent_name)
                print(agent.target_name)
                print(agent.capture())
                while not agent.capture():
                    if verbose:
                        print(
                            "Step {}, agent at {}, target at {}".format(
                                num_steps, agent.agent_name, agent.target_name
                            )
                        )
                    if visualize:
                        agent.plot(step=num_steps + 1)
                    agent.move_target()
                    if visualize:
                        agent.plot(step=num_steps + 1)
                    agent.move_agent()
                    num_steps += 1
                self.results[Agent.__name__] += [num_steps]

                if verbose:
                    print(
                        "{} found the target in {} steps.".format(
                            Agent.__name__, num_steps
                        )
                    )

                if visualize:
                    # figs to video
                    figs = os.listdir("../results/figs")
                    # sort the figs by the time they are created
                    figs.sort(key=lambda x: os.path.getmtime("../results/figs/" + x))
                    images = []
                    for fig in figs:
                        images.append(imageio.imread("../results/figs/" + fig))
                    imageio.mimsave(
                        "../results/videos/{}.mp4".format(Agent.__name__), images, fps=2
                    )
                    # delete all the figs
                    for fig in figs:
                        os.remove("../results/figs/" + fig)

        for key in self.results.keys():
            print(
                "The average number of steps for {} is {} with std {}".format(
                    key, np.mean(self.results[key]), np.std(self.results[key])
                )
            )


if __name__ == "__main__":
    args = parse_args()
    squad_str = "["
    for num in args.agents:
        squad_str += "GraphAgent" + str(num) + ","
    squad_str = squad_str[:-1] + "]"
    squad_list = eval(squad_str)
    test = Simulation(squad=squad_list, num_simulations=args.num_simulations)
    test.run(visualize=args.visualize, verbose=args.verbose)
