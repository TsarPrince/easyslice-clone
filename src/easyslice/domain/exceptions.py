class EasySliceError(Exception):
    """Base exception for easyslice."""


class AiResponseSchemaError(EasySliceError):
    """Raised when the AI returns JSON that doesn't match the expected schema."""


class ExternalToolError(EasySliceError):
    """Raised when an external tool (ffmpeg, yt-dlp, etc.) fails."""
