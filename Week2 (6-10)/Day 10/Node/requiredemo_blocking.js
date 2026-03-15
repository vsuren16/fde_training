const fs = require('fs');
 
const data = fs.readFileSync('data01.txt', 'utf-8');

console.log(data);
console.log("Finished reading file");