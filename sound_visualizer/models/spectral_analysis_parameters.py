from typing import Optional

from pydantic import BaseModel, Field


class SpectralAnalysisParameters(BaseModel):
    # one, or the other
    youtube_url: Optional[str]
    filename: Optional[str]

    overlap_factor: float = Field(ge=0.0, le=0.999999, default=0.9)
    frame_size_power: int = Field(ge=8, le=20, default=12)
