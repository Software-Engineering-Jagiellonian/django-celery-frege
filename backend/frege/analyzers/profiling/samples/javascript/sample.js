(function () {
  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[getRandomInt(0, 15)];
    }
    return color;
  }

  function createRandomArray(length) {
    return Array.from({ length }, () => getRandomInt(1, 100));
  }

  function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = getRandomInt(0, i);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  const arr = createRandomArray(10);
  console.log("Original:", arr);
  console.log("Shuffled:", shuffleArray([...arr]));
  console.log("Random color:", getRandomColor());
})();
