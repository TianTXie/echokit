class PlainTextOutputSpeech:
    """Plaintext-formatted output speech"""

    def __init__(self, text):
        self.type = 'PlainText'
        self.text = text

    def _dict(self):
        return self.__dict__


class SSMLOutputSpeech:
    """SSML-formatted output speech"""

    def __init__(self, ssml):
        self.type = 'ssml'
        self.ssml = ssml

    def _dict(self):
        return self.__dict__
