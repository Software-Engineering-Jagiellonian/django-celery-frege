function computeMax(data, modulo) {
    // Compute a modulo sum array. Store an index and a sum.
    var sums = [[-1, 0]];
    var maxSum = 0;
    for (var i=0; i<data.length; i++) {
        sums.push([i, (sums[i][1] + data[i]) % modulo]);
        // One can always compute the difference between 0 and the current element.
        maxSum = Math.max(sums[sums.length-1][1], maxSum);
    }
    // Sort the array by sum value.
    sums.sort(function(a,b){return a[1]-b[1];});

    for (var i=1; i<sums.length; i++) {
        var origIndex = sums[i][0],
            curSum = sums[i][1];
        // Look for the first element with greater sum with index before it.
        var j = i+1;
        while (j<sums.length && (sums[j][0] >= origIndex || sums[j][1] == curSum)) {
            j++;
        }
        // If we found one, compute the negative difference and update max.
        if (j<sums.length) {
            maxSum = Math.max(curSum - sums[j][1] + modulo, maxSum);
        }
    }
    return maxSum;
}

function processData(input) {
    var data = input.split("\n");
    var t = Number(data[0]);
    for (var i=0; i<t; i++) {
        var m = Number(data[i*2+1].split(" ")[1]);
        var vals = data[i*2+2].split(" ").map(Number);
        console.log(computeMax(vals, m));
    }
}

process.stdin.resume();
process.stdin.setEncoding("ascii");
_input = "";
process.stdin.on("data", function (input) {
    _input += input;
});

process.stdin.on("end", function () {
   processData(_input);
});
