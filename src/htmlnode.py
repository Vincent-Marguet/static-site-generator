"""
HTMLNode Parent class module
"""


class HTMLNode:
    """
    Parent class to handle HTML Node
    - tag is a string representing the HTML tag name (e.g "p", "a", "h1"...)
    - value is a string representing the value of the HTML tag (e.g the text inside a paragraph)
    - children is a list of HTMLNode objects representing the children of this particular node
    - props is a dictionnary of key-value pairs representing the attributes of the HTML tag.
    For example a link(<a> tag) might have {"href": "https://www.google.com"}

    All attributes are defaulted to None because :
    - An HTMLNode without a tag will just render as raw text
    - An HTMLNode without a value will be assumed to have children
    - An HTMLNode without children will be assumed to have a value
    - An HTMLNode without props simply won't have any attributes
    """

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self._tag = tag
        self._value = value
        self._children = []
        self._props = props
        self.children = children

    @property
    def tag(self):
        """
        Getter for tag member
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @property
    def value(self):
        """
        Getter for value member
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def children(self):
        """
        Getter for children member
        """
        return self._children

    @children.setter
    def children(self, children):
        if children is not None and not all(
            isinstance(child, HTMLNode) for child in children
        ):
            raise ValueError("All children must be instances of HTMLNode.")
        self._children = children if children is not None else []

    @property
    def props(self):
        """
        Getter for props member
        """
        return self._props

    @props.setter
    def props(self, props):
        if props is not None and not isinstance(props, dict):
            raise ValueError("Props must be a dictionary.")
        self._props = props

    def to_html(self):
        """
        This method must be override by subclasses
        """
        raise NotImplementedError("This method must be override by children")

    def props_to_html(self):
        """
        Returns a string that represents the HTML attributes
        of the node (handles nested dictionaries).
        """

        def process_dict(d):
            if not d:  # Base case: no attributes
                return ""

            attributes = []
            for key, value in d.items():
                if isinstance(value, dict):  # Handle nested dictionaries
                    if key == "style":
                        # Flatten style dict properly
                        style_string = "; ".join(
                            [f"{k}:{v}" for k, v in value.items()])
                        attributes.append(f'{key}="{style_string}"')
                    else:
                        nested = process_dict(
                            value
                        ).strip()  # No leading/trailing space in nested
                        attributes.append(f'{key}="{nested}"')
                else:
                    # Standard key-value pair
                    attributes.append(f'{key}="{value}"')
            return " ".join(attributes)  # Join attributes with a single space

        # Call the recursive helper with self.props
        if not self.props:
            return ""
        return " " + process_dict(self.props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        return False
