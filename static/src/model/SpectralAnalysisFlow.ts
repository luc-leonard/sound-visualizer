export class SpectralAnalysisParameters {
    constructor(
        public youtube_url: string,
        public overlap_factor: number,
        public frame_size_power: number) {
    }
}

export class SpectralAnalysisResult {
    constructor(
        public width: number,
        public tile_width: number,
        public height: number
    ) {
    }
}

export class SpectralAnalysisFlow {
    constructor(
        public id: String,
        public parameters: SpectralAnalysisParameters,
        public stopwatches: Map<string, number>,
        public memory_used: Map<string, number>,
        public status: string,
        public result: SpectralAnalysisResult,
    ) {
    }
}
