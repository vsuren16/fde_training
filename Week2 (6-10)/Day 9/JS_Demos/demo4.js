//Scenario1: online food ordering app 

// //filter: used to select only delivered orders
// let const_orders = [
//     {customer: "Amit", items:3, delivered: true},
//     {customer: "Sara", items:5, delivered: false},
//     {customer: "John", items:2, delivered: true},
//     {customer: "Priya", items:4, delivered: true}
// ];
// let delivered_orders = const_orders.filter(order => order.delivered === true);
// console.log(delivered_orders)

// //extract names
// let extract_names = const_orders.map(names => names.customer)
// console.log(extract_names)

// //reduce(): used to give total items delivered
// let total_delivered_orders = delivered_orders.reduce((sum,orders) => {return sum+orders.items; },1);
// console.log(total_delivered_orders)

//Scenario2: E-comm price calculator 
//rest operator 


function calculateTotal(percent,...num){
    let total = 0;
    for (let i of num){
        total += i;
    }
    return total;

}
console.log(calculateTotal(10,20,30))

calculateTotal2 = (...num) => { total=0; for (let i of num){total += i} return total}
console.log(calculateTotal2(10,20))