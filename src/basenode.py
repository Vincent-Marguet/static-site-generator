"""
Pure abstract class for Nodes
"""

from abc import ABC, abstractmethod

from src.textnode import TextNode, TextType


class BaseNodes(ABC):
    """
    Abstract class for nodes
    """

    @classmethod
    def parse(cls, text):
        """
        General parsing pipeline that can be reused by all formats.
        Subclasses override specific splitting steps.
        """
        # Starts with a single, undifferentiated TextNode
        nodes = [TextNode(text, {TextType.NORMAL})]
        # Calls subclass-implemented methods to refine nodes
        nodes = cls.split_nodes_image(nodes)
        nodes = cls.split_nodes_link(nodes)
        nodes = cls.split_nodes_delimiter(nodes)
        return nodes

    @classmethod
    @abstractmethod
    def split_nodes_image(cls, nodes):
        """
        Subclasses must implement image splitting.
        """
        raise NotImplementedError("this method must be override by children")

    @classmethod
    @abstractmethod
    def split_nodes_link(cls, nodes):
        """
        Subclasses must implement link splitting.
        """
        raise NotImplementedError("this method must be override by children")

    @classmethod
    @abstractmethod
    def split_nodes_delimiter(cls, nodes):
        """
        Subclasses must implement delimiter parsing
        """
        raise NotImplementedError("this method must be override by children")
