export class RandomStringGenerator{
    constructor(
        private seed: Number
    ) {

    }

    generateRandomString(): string {
        return this.seed.toString()
    }
}