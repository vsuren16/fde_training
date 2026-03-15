//Array access 
let arrnumbers = [10, 20, 30]; 
console.log(arrnumbers[1]);

arrnumbers.push(40);
console.log(arrnumbers);

//Destructuing 
//Object Destructuring

//object 
vuser = { 
    name : "Hike",
    age:25
}

const {name:vusername, age:vuserage} = vuser;
console.log(vusername);

//array destructuing 
let colours = ["red","blue","black"]
const [first, second] = colours;
console.log(first)
console.log(second)

//Spread Operator 
//copy array
let arr1 = [1,2];
let arr2 = [...arr1,3]
let arr3 = [4,...arr1,0,-1]
console.log(arr2);
console.log(arr3);

let firstname = {name: "Suren"};
let fullname = {...firstname, lastname: "V"}
console.log(fullname);

//map(): used to transform each item 
let arr2numbers = [1,2,3];
let doubled = arr2numbers.map(num => num*2);
console.log(doubled);

//filter: used to select items
let arr3numbers = [1,2,3,4];
let evenNumbers = arr3numbers.filter(num => num %2 === 0);
console.log(evenNumbers)

//reduce(): used to combine values 
let numbers = [1,2,3,4];
let sum = numbers.reduce((total,num) => {return total-num; },0);
console.log(sum)