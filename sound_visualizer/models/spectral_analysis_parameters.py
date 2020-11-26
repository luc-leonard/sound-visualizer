from typing import Optional

from pydantic import BaseModel, Field


class SpectralAnalysisParameters(BaseModel):
    # one, or the other
    youtube_url: Optional[str]
    filename: Optional[str]

    start_second: Optional[int] = 0
    length_second: Optional[int] = -1
    overlap_factor: Optional[float] = Field(ge=0.0, le=0.95, default=0.8)
    frame_size_power: int = Field(ge=12, le=18, default=14)
