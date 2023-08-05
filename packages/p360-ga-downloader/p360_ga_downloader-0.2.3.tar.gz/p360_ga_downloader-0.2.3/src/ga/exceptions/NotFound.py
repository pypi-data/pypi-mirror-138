import google


class NotFound(google.api_core.exceptions.NotFound):
    """ Just wrapping the google code for loosing the coupling in upper code """
