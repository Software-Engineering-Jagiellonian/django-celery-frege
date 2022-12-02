import * as readline from 'node:readline';

const fibbonaci = (n: number, numbersSoFar?: {[key: number]: number}): number => {
    if (numbersSoFar === undefined) {
        numbersSoFar = {}
    }

    if (n in numbersSoFar) {
        return numbersSoFar[n];
    }

    if (n < 2) {
        numbersSoFar[n] = n;
    }
    else {
        const resultForN = fibbonaci(n - 1, numbersSoFar) + fibbonaci(n - 2, numbersSoFar);
        numbersSoFar[n] = resultForN;
    }

    return numbersSoFar[n];
}

let rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

rl.question("Input fibbonaci number you would like to see: ", (answer: string) => {
    const n: number = parseInt(answer);
    console.log(fibbonaci(n));
})
