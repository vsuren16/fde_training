function add(a,b) { 
    return a+b;
}
module.exports = add; 

export function substract(a,b) {
    return a-b;
}

export default function multiply(a,b) {
    return a*b;
}


//OR -- EITHER WE CAN EXPORT THE FUNCTION LIKE THIS or we can export it like the above way. Both are correct.

// export function add(a,b) {
//     return a+b;
// }