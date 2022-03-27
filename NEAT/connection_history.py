from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from NEAT.genome import Genome
    
from NEAT.node import Node


class ConnectionHistory:
    '''Containes history of prior mutations and innovations,
    This is used to determine if a certain mutation is innovative or not
    :param from_number: number of start node for the gene
    :param to_number: number of targeet node of the gene
    :param innovation_history: global list of all previous mutations
    :prior_innovations: previous innovations of the gene's genome
    '''

    def __init__(self, from_number: int, to_number: int, innovation_number: int, prior_innovations: list[int]) -> None:
        self.__from_number = from_number
        self.__to_number = to_number
        self.__innovation_number = innovation_number
        self.__prior_innovations = prior_innovations.copy()

    def matches(self, genome: Genome, from_node: Node, to_node: Node) -> bool:
        '''Returns whether the given genome mathces the original genome
        and the connections are between the same nodes.
        Two genomes are considered matching if all prior innovations
        of the original genome untill this mutation are included in the given one
        :param genome: genome to compare the history to
        :param from_node: start node of the compared gene
        :param to_node: target node of the compared gene
        '''

        # Check if the numbers of connections are the same
        if len(genome.genes) != len(self.__prior_innovations):
            return False

        # Check if the connecting nodes have the same number
        if from_node.number != self.__from_number or to_node.number != self.__to_number:
            return False

        # Next check if all of the innovation numbers match from the genome
        return all(gene.innovation_number in self.__prior_innovations for gene in genome.genes)

    @property
    def innovation_number(self) -> int:
        return self.__innovation_number