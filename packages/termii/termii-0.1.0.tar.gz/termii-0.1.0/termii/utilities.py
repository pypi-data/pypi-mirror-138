class WrongMediaOptions(Exception):
    """
    Exception raised for not enough options in media dictionary

    Attributes:
    message: str
        Message to be printed to the user
    """

    def __init__(self, message="'url' and 'caption' keys must be found in the media dictionary"):
        self.message = message
        super().__init__(self.message)

class WrongType(Exception):
    """
    Exception raised for wrong type

    Attributes:
    trigger: str
        Feature which triggers the exception
    dtype: str
        The type to be included in the message
    message: str
        Message to be printed to the user
    """

    def __init__(self, dtype, trigger):
        self.dtype = dtype
        self.trigger = trigger
        self.message = f"Datatype of {trigger} must be {dtype}"
        super().__init__(self.message)