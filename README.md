# ai-toolbox

## Project Vision
The general vision for this project is, to build an extensible framework of AI-components, which can be linked
together, to realize intelligent software agents. Additionally, simulation environments should be implemented,
in which the agents can learn through reinforcement learning and performance can be evaluated. As an in-between step to
such complex simulations, the framework should feature a logging mechanism, which can be used to create plots, for 
visualizing the agent's behavior.

## Current State
In its current state, the project is less of a framework, but more of an architectural guideline, of how the components 
should be implemented and used, to realize intelligent agents. The guidelines are showcased by a simple example. It 
demonstrates how the components are intended to interact with each other, how the agent interacts with an environment 
and how results are logged and visualized.

## Architectural Description
The central building block of an intelligent agent is the `component`. Each component is responsible for a certain task.
It has zero or more input streams and one or more output streams. The components interact, by connecting output streams 
of one component, to the input streams of another component. There are no limitations of how a component is implemented,
but generally they should make use of neural networks, or itself be building blocks of neural networks, to better mimic
how real brains work. 

The agent interacts with the `environment`, by attaching output signals of one or more components, to controllable 
handles the environment provides. The agent perceives in the environment, by feeding information into the input streams
of one or more components.

The agent learns by making sense of the input signals it receives from the environment, as a result of the output
signals it has previously sent to the environment.

Sometimes it can be necessary to decouple the firing rate of a component's output from the rate of its received inputs. 
In such a case the global `timer` is used. It produces a stream of ticks, such that any component can react with a set
frequency. For an example of how this can be useful look at the `cpg` component, that produces a movement pattern, at a
much higher frequency, than the frequency of its input signals.

The behavior of an agent is visualized, by attaching `loggers` to its components' output streams and later plotting
the results. Alternatively, the environment could feature a visual representation of the agent's interactions.

## Description of Demo
The current example implementation shows the intended architecture for building an agent within this framework. It features an 
example agent consisting of 4 components (`components/`), an environment (`core/env.py`), logging (`core/logger.py`) and 
plotting (`run/log_visualization.py`) functionalities. In `run/component_test.py` the main entry point to this 
example can be found. There, the agent is assembled together, the environment is set up and the and the logging is
attached to both the environment and the agent. The logged data is plotted in the file `run/log_visualization.py`.

The agent consists of the four components - a visual component `components/visual.py`, an evaluator component 
`components/eval.py`, a random pattern generator (RPG) component `components/rpg.py` and a central pattern generator (
CPG) component `components/cpg.py`. The visual component periodically receives random cat/dog images from the environment 
`core/env.py`, to simulate different animals approaching the agent. The visual component contains a neural network 
classifier to determine whether a cat or dog is present and which type. The result is sent to the evaluation component, 
which determines danger and opportunity levels, based on the classifications. Cats are considered good and dogs are considered
dangerous. The CPG component activates one of two movement patterns, which should indicate that the agent is running
towards cats and runs away from dogs. Additionally, the results of the evaluator component are sent to the RPG component,
which has a chance to inverse the movement pattern choice of the CPG component. 

The general data flow goes from images, randomly selected by the environment and periodically sent to the agent, through 
the components of the agents, back to the environment, in the form of actions taken. All the while the data flow is 
logged to a file (see log/logfile.txt for an example). The data flow looks like this: `env -> visual -> eval -> cpg -> 
env`, with an additional route `eval -> rpg -> cpg`

Timekeeping is done by a global timer `core/timer.py`. Time is measured in ticks. The tick rate can be configured in 
ticks per second. The timer is used by the environment, the CPG and the Logger.

The simulation environment `core/env.py` periodically selects a random image from a pool of 5 cat and 5 dog images. The
frequency is configurable by setting the tick rate with which new images load. In this demo, limbs of the agent are 
considered as part of the environment. The agent's CPG periodically sends muscle activation signals to the limbs. The 
frequency of those signals is also configurable, based on the tick rate of the global timer.

The Logger `core/logger.py` is attached to each of the agent's components output streams. It logs the received values
to `log/logfile.txt` in a comma separated format. After the simulation is done, the logs can be visualized by running
`run/log_visualization.py`. Additionally, a demo graph can be plotted, by running component_test.py with 
`demo_mode = True` and plotting the results.

## Ideas for Further Advancement
Multiple important sub-goals need to be achieved, for realising the project vision. 
1) Simulation capabilities + Evaluation: Currently, simulation capabilities are very limited. A graphical simulation,
of the agent in the environment (2D or 3D) should be implemented. 
2) Re-usability of components: Currently, re-usability of components is severely restricted, since they are very specific
and expect very specific input values. In the future components should be made much more general purpose. This could be 
achieved by having many more and much smaller components interacting together, instead of a few larger, very specific 
ones. 
3) Reinforcement learning for components: Currently, no reinforcement learning is used, to adjust the weights of 
neural networks inside the component. All components rely on loaded pre-trained models. In the future, the agent should
be able to learn both, from the environment feedback and also from component feedback.
4) Dynamic component topologies: Currently, a human expert needs to carefully put together the components manually, to 
solve a certain task with the agent. In the future, the agent should be able to dynamically add/remove components from 
a pool of available components and also be able to form new connections, or remove connections, between its components.
As long as the agent's topology is fixed, we do not have real intelligence.

## Licence
This project is licenced under the GNU General Public License v3.0