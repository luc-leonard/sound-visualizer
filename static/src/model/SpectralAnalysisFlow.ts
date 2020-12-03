export class SpectralAnalysisParameters {
    constructor(
        public youtube_url: string,
       public  start_second: number,
        public length_second: number,
        public overlap_factor: number,
        public frame_size_power: number) {
    }
}

export class SpectralAnalysisFlow {
    constructor(
        public id: String,
        public parameters: SpectralAnalysisParameters,
        public stopwatches: Map<string, number>,
        public memory_used: Map<string, number>,
        public status: string
    ) {}
}
