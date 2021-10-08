from __future__ import annotations

import numpy as np
import math

from typing import List

class NeuralNetwork:
    def __init__(self, a: int | NeuralNetwork, b: List[int] = None, c: int = None, d: int = None) -> None:
        if isinstance(a, NeuralNetwork):
            # Copy model
            self.__shape = a.shape
            self.__weights = a.weights.copy()
            self.__biases = a.biases.copy()
        else:
            # Create model
            self.__shape = (a, b, c)
            
            self.__weights = [
                np.random.uniform(-1, 1, size=(self.__shape[1::-1])), # Hidden to input
                np.random.uniform(-1, 1, size=(self.__shape[:0:-1])), # Output to hidden
            ]

            self.__biases = [
                np.random.uniform(-1, 1, size=(self.__shape[1],)), # Hidden biases
                np.random.uniform(-1, 1, size=(self.__shape[2],)), # Output biases
            ]

            self.mutate(0.1)

    def predict(self, inputs: List[float]) -> List[float]:
        input = np.array(inputs)

        # Generate hidden output
        output = self.Tanh(np.dot(self.__weights[0], input) + self.__biases[0])

        # Generate final output
        output = self.Sigmoid(np.dot(self.__weights[1], output) + self.__biases[1])

        print(output)
        return output
        
    def copy(self) -> NeuralNetwork:
        return NeuralNetwork(self)

    def mutate(self, rate: float) -> None:
        mutate_value = lambda val, rate: val + np.random.normal() \
            if np.random.random() < rate else val

        self.__weights = [mutate_value(arr, rate) for arr in self.__weights]

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.__shape

    @property
    def weights(self) -> List[np.ndarray[float]]:
        return self.__weights

    @property
    def biases(self) -> np.ndarray[float]:
        return self.__biases

    @property
    def Tanh(self) -> np.vectorize:
        return np.vectorize(math.tanh)

    @property
    def Sigmoid(self) -> np.vectorize:
        return np.vectorize(lambda x: 1 / (1 + math.exp(-x)))
    