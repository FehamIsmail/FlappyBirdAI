# FlappyBirdAI
This is a simple implementation of the popular game Flappy Bird using the Pygame library. The AI uses a genetic algorithm to learn how to play the game.
It can be both played in machine learning mode or in a regular mode. 

## Requirements
- Python 3.x
- Pygame

## How to Run

1. Clone the repository:
```
git clone https://github.com/FehamIsmail/FlappyBirdAI.git
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the game:
```
python main.py
```

## How to Play

- The AI will play the game automatically and will try to learn how to play it better over time
- You can also play the game manually by toggling the variable `MACHINE_LEARNING_MODE` to `False`


## Neural Network 
The neural network used in this implementation is a simple feedforward neural network with one hidden layer. 
The input to the network is the distance of the bird from the next pipe and the network's output is the flap 
or no flap action. The network is trained using a genetic algorithm where the weights and biases of the network 
are evolved to play the game better over time. The genetic algorithm works by creating a population of networks
with random weights and biases, and then selecting the best performing networks to breed and create the next 
generation. The process of breeding and mutating the networks continues until a satisfactory level of performance
is achieved.

The network uses the sigmoid activation function in the hidden layer and output layer. This function maps the 
input to a value between -1 and 1, which represents the probability of the bird flapping its wings. 


