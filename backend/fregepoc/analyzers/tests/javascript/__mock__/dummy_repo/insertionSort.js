function processData(input) {
    //Enter your code here
    var input_arr = input.split('\n');
    var tests = parseInt(input_arr[0],10);

    for (var i = 1; i < tests*2; i+=2) {
        var n = parseInt(input_arr[i], 10);
        var arr = input_arr[i+1].split(' ');
        var count = countInversions(arr);

        process.stdout.write(count + '\n');
    }
};

function countInversions(arr) {
  var count = 0;

  function mergeSort(arr, length) {
    if (length < 2) { return arr; }
    var middle = Math.ceil(length/2);
    var left = mergeSort(arr.slice(0,middle),middle);
    var right = mergeSort(arr.slice(middle), length - middle);
    var merged = [];
    count += merge(left, right, merged, length);
    return merged;
  };

  mergeSort(arr, arr.length);
  return count;
};


function merge(left, right, merged, length) {
  var l = 0;
  var r = 0;
  var inversions = 0;

  for (var m = 0; m < length; m++) {
    if (right[r] === undefined || parseInt(left[l], 10) <= parseInt(right[r], 10)) {
      merged[m] = left[l];
      l++;
    } else {
      merged[m] = right[r];
      r++;
      inversions += left.length - l;
    }
  }

  return inversions;
};

process.stdin.resume();
process.stdin.setEncoding("ascii");
_input = "";
process.stdin.on("data", function (input) {
    _input += input;
});

process.stdin.on("end", function () {
   processData(_input);
});
