from typing import Dict, Callable

class AssistantRegistry:
    """
    A registry for managing and retrieving assistant implementations dynamically.
    Each assistant must be registered with a unique name and a function that 
    builds the assistant using an LLM model.
    """

    _registry: Dict[str, Callable] = {}

    @classmethod
    def register_assistant(cls, name: str, builder: Callable):
        """
        Register an assistant with a unique name.

        Args:
            name (str): Unique identifier for the assistant.
            builder (Callable): A function that takes an LLM instance and returns the assistant.

        Raises:
            ValueError: If an assistant with the same name is already registered.
        """
        if name in cls._registry:
            raise ValueError(f"Assistant '{name}' is already registered.")
        cls._registry[name] = builder

    @classmethod
    def get_assistant(cls, name: str, llm):
        """
        Retrieve and build an assistant by name.

        Args:
            name (str): The name of the registered assistant.
            llm: The LLM model instance to be used by the assistant.

        Returns:
            The built assistant instance.

        Raises:
            KeyError: If the requested assistant is not found.
        """
        if name not in cls._registry:
            raise KeyError(f"Assistant '{name}' is not registered.")
        return cls._registry[name](llm)

    @classmethod
    def list_assistants(cls):
        """
        List all registered assistants.

        Returns:
            List of registered assistant names.
        """
        return list(cls._registry.keys())