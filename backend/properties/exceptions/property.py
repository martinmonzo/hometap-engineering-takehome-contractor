class PropertyException(Exception):
    """Custom exception for property errors."""

    class ErrorCode:
        """Add below more possible errors"""
        Address_Required = ("Address is required", 400)
        Unauthorized = ("Unauthorized", 401)
        Unknown_Error = ("Unknown Error", 500)

    def __init__(self, error_code):
        self.message, self.status_code = error_code
        super().__init__(self.message)

    def to_dict(self):
        return {"error": self.message}
