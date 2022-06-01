// We define the similarity of the strings to be
// the length of the longest prefix common to both strings
var calculateSimilarity = function (s, substring) {
    var L = substring.length;
    var pos = 0;
    var result = 0;

    match = s[pos] === substring[pos];

    while (match) {
        pos += 1;
        match = match = s[pos] === substring[pos] && pos < L;
    }

    return pos;
}

var substrings = function (s) {
    var results = [];
    var i = 1;
    var l = s.length;

    while (i <= l) {
        results.push(s.substr(i));
        i++;
    }

    return results;
}

var zFunction = function (s) {
    var l = 0,
        r = 0,
        n = s.length,
        z = [s.length];

    for (var i = 1; i < n; i++) {
        if (i > r) {
            l = r = i;
            while (r < n && s[r-l] == s[r]) {
                r++;
            }
            z[i] = r-l;
            r--;
        } else {
            var k = i-l;
            if (z[k] < r-i+1) {
                z[i] = z[k];
            } else {
                l = i;
                while (r < n && s[r-l] == s[r]) {
                    r++;
                }
                z[i] = r-l;
                r--;
            }
        }
    }

    return z;
}

function processData (input) {
    var lines = input.split('\n');
    var T = lines[0];

    for (var i=1; i<=T; i++) {
        var line = lines[i];
        var z = zFunction(line);
        var sum = z.reduce(function(prev, next) {
            return prev + next;
        });
        console.log(sum);
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
