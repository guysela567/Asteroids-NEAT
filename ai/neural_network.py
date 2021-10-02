from __future__ import annotations

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Sequential
import random

from typing import List

class NeuralNetwork:
    def __init__(self, a: int or Sequential, b: List[int], c: int, d: int = None) -> None:
        if isinstance(a, Sequential):
            self.__model = a;
            self.__input_nodes = b;
            self.__hidden_nodes = c;
            self.__output_nodes = d;
        else:
            self.__input_nodes = a;
            self.__hidden_nodes = b;
            self.__output_nodes = c;
            self.__model = self.__create_model()

    def __create_model(self) -> Sequential:
        return Sequential([
            layers.Dense(self.__hidden_nodes[0], activation='relu', input_shape=(1,)),
            *[layers.Dense(no, activation='relu') for no in self.__hidden_nodes[:-1]],
            layers.Dense(self.__output_nodes),
        ])
        
    def copy(self) -> NeuralNetwork:
        model_copy = self.__create_model()
        model_copy.set_weights(self.weights)
        return NeuralNetwork(model_copy, self.__input_nodes, self.__hidden_nodes, self.__output_nodes)

    def mutate(self, rate: float) -> None:
        def mutate_value(val: float, rate: float) -> float:
            return val + np.random.normal() if random.random() < rate else val
        
        self.weights = [mutate_value(arr, rate) for arr in self.weights]

    @property
    def model(self) -> Sequential:
        return self.__model

    @property
    def weights(self) -> List[np.ndarray[float]]:
        return self.__model.get_weights()

    @weights.setter
    def weights(self, weights: List[np.ndarray[float]]) -> None:
        self.__model.set_weights(weights)
