function sayHello(){
    console.log("We are learing ES6")
}

function sayHellotoName(name){
    console.log("Hello "+name)
}

function sayHellotoName2(name){
    console.log(`Hello ${name}, Welcome to ES6!`)
}

sayHello() 
sayHellotoName("Suren")
sayHellotoName2("Suren")


//arrow functions 
sayadd = (a,b) => a+b;
result = sayadd(5,10)
console.log(`Sum of a+b is ${result}!`)

checkevenorodd = (num) => num % 2 === 0 ? true : false
console.log(checkevenorodd(4)) 

//rest operator 

function calculateTotal(...num){
    let total = 0;
    for (let i of num){
        total += i;
    }
    return total;

}
console.log(calculateTotal(10,20,30))

calculateTotal2 = (...num) => { total=0; for (let i of num){total += i} return total}
console.log(calculateTotal2(10,20))