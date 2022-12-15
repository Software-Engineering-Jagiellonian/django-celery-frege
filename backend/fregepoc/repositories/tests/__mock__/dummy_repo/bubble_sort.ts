type listOfNums = number[]

/*
    function that performs bubble sort
    it does not modify original array
*/
const bubbleSort = (original: listOfNums): listOfNums => {
    let workingArr: listOfNums = [...original]; //copying array in order not to modify original

    for(let i: number = 0; i < workingArr.length - 1; i++) {
        for (let j: number = 0; j < workingArr.length - i - 1; j++) {
            if (workingArr[j] > workingArr[j + 1]) {
                //nice way of swapping values
                [workingArr[j], workingArr[j + 1]] = [workingArr[j + 1], workingArr[j]]
            }
        }
    }

    return workingArr
}
