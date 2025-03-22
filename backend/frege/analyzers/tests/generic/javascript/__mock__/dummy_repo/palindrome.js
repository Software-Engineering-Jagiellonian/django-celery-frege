"use strict";

const fs = require("fs");

process.stdin.resume();
process.stdin.setEncoding("utf-8");

let inputString = "";
let currentLine = 0;

process.stdin.on("data", inputStdin => {
  inputString += inputStdin;
});

process.stdin.on("end", _ => {
  inputString = inputString
    .trim()
    .split("\n")
    .map(str => str.trim());

  main();
});

function readLine() {
  return inputString[currentLine++];
}

/*
 * Complete the buildPalindrome function below.
 */
// Object to save status of each characters
function State() {
  let link = -1;
  let posStart = 0;
  let childs = {};
  return {
    link,
    posStart,
    childs
  };
}

// reverse the string
function reverseString(str) {
  const res = [];
  for (let i = 0, len = str.length; i <= len; i++)
    res.push(str.charAt(len - i));
  return res.join("");
}

// Cut the string into characters and store the position of the character at the variable StateState
function buildState(a) {
  let states = Array.from({ length: 2 * a.length }, () => State()); //caching
  let last = 0,
    start = 1;
  for (let i = 0; i < a.length; i++) {
    const char = a[i];
    const cur = start;
    start++;
    states[cur].posStart = states[last].posStart + 1;
    let p = last;

    while (p !== -1 && !states[p].childs[char]) {
      states[p].childs[char] = cur;
      p = states[p].link;
    }

    if (p === -1) states[cur].link = 0;
    else {
      const q = states[p].childs[char];
      if (states[p].posStart + 1 === states[q].posStart) states[cur].link = q;
      else {
        const clone = start;
        start++;

        //copy older element state
        states[clone].posStart = states[p].posStart + 1;
        states[clone].childs = { ...states[q].childs };
        states[clone].link = states[q].link;

        while (p !== -1 && states[p].childs[char] === q) {
          states[p].childs[char] = clone;
          p = states[p].link;
        }
        states[q].link = clone;
        states[cur].link = clone;
      }
    }
    last = cur;
  }
  return states;
}
// build palindrome to look up
function lookupPalin(s) {
  const len = s.length;
  let sx = "|"; // cut the string into pieces: ex: |h|e|l|l|o|
  const sxlen = len * 2 + 1;
  for (let i = 0; i < len; i++) sx += s[i] + "|";

  let res = Array.from({ length: sxlen }, () => 0);

  let c = 0,
    r = 0,
    m = 0,
    n = 0;

  for (let i = 1; i < sxlen; i++) {
    if (i > r) {
      res[i] = 0;
      m = i - 1;
      n = i + 1;
    } else {
      const i2 = c * 2 - i;
      if (res[i2] < r - i) {
        res[i] = res[i2];
        m = -1;
      } else {
        res[i] = r - i;
        n = r + 1;
        m = i * 2 - n;
      }
    }
    while (m >= 0 && n < sxlen && sx[m] === sx[n]) {
      res[i] += 1;
      m -= 1;
      n += 1;
    }
    if (i + res[i] > r) {
      r = i + res[i];
      c = i;
    }
  }
  let result = Array.from({ length: len }, () => 0);
  for (let i = 1; i < sxlen - 1; i++) {
    const idx = parseInt((i - res[i]) / 2);
    result[idx] = Math.max(result[idx], res[i]);
  }
  return result;
}

// check ordre asc string
function check(s, initial, posStart, size) {
  for (let i = 0; i < size; i++) {
    if (s[initial + i] !== s[posStart + i]) {
      if (s[initial + i] > s[posStart + i]) return true; //
      break;
    }
  }
  return false;
}

function solve(a, b) {
  const blen = b.length;
  const states = buildState(a);

  let plookup = lookupPalin(b);

  let apos = 0,
    start = -1,
    left = 0,
    mid = 0,
    total = 0,
    curlen = 0;

  // find the position's index  of the palindrome start character
  for (let i = 0; i < blen; i++) {
    const char = b[i];
    if (!states[apos].childs[char]) {
      while (apos !== -1 && !states[apos].childs[char])
        apos = states[apos].link;
      if (apos === -1) {
        apos = 0;
        curlen = 0;
        continue;
      }
      curlen = states[apos].posStart;
    }

    curlen += 1;
    apos = states[apos].childs[char];
    const new_start = i - curlen + 1;
    let new_mid = 0;
    if (i + 1 < blen) new_mid = plookup[i + 1];
    const new_total = 2 * curlen + new_mid; //total length of such a substring palindrome

    if (
      total < new_total ||
      (total === new_total && check(b, start, new_start, curlen + mid))
    ) {
      left = curlen;
      mid = new_mid;
      total = new_total;
      start = new_start;
    }
  }

  // find palindrome
  let palindrome = [];
  for (let i = 0; i < left + mid; i++) palindrome.push(b[start + i]); // push string containt le palindrome
  for (let i = left - 1; i > -1; i--) palindrome.push(palindrome[i]); // push string can be reverse in other string
  return palindrome.join("");
}

function buildPalindrome(a, b) {
  const reverseB = reverseString(b);
  const res1 = solve(a, reverseB);
  const len1 = res1.length;
  const res2 = solve(reverseB, a);
  const len2 = res2.length;
  let res;
  if (len1 > len2) res = res1;
  else if (len1 < len2) res = res2;
  else res = res1 < res2 ? res1 : res2;
  if (res.length === 0) return -1;
  return res;
}

function main() {
  const ws = fs.createWriteStream(process.env.OUTPUT_PATH);

  const t = parseInt(readLine(), 10);

  for (let tItr = 0; tItr < t; tItr++) {
    const a = readLine();

    const b = readLine();

    let result = buildPalindrome(a, b);

    ws.write(result + "\n");
  }

  ws.end();
}
