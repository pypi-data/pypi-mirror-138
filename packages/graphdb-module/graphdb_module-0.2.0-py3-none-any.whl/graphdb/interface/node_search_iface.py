from abc import ABC, abstractmethod
from typing import List

from graphdb.schema import Node


class NodeSearchInterface(ABC):
    """Base class for basic operation search or read node"""

    @abstractmethod
    def find_node(
            self,
            node: Node,
            limit: int = 100,
    ) -> List[Node]:
        """Find node with specified parameters
        :param node: object node
        :param limit: default limit query
        :return: list of object node
        """
        raise NotImplementedError
