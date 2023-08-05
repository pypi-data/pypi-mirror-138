class PipelineInternalError(RuntimeError):
    def __init__(self, message: str):
        super(PipelineInternalError, self).__init__(message)


class PipelineInputError(RuntimeError):
    def __init__(self, message: str):
        super(PipelineInputError, self).__init__(message)
