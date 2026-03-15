// function preparePizza(callback) {
//     setTimeout(() => {
//         console.log("Pizza is ready!");
//         callback();
//     },3000);
// }

// // function notifyCustomer() { 
// //     console.log("Notifying customer...");
// // }

// ////single callback
// //preparePizza(notifyCustomer);

// function notifyCustomer(callback) { 
//     console.log("Notifying customer...")
//     callback();
// }

// function deliveryPizza() {
//     setTimeout(() => {console.log("Pizza Delivered"); },2000);
// }

// //nesting of callbacks
// preparePizza(() => {
//     notifyCustomer(() => {
//         deliveryPizza();
//     });
// });

//3 - Customer feedback addition

function preparePizza(callback) {
    setTimeout(() => {
        console.log("Pizza is ready!");
        callback();
    },3000);
}

function notifyCustomer(callback) { 
    console.log("Notifying customer...")
    callback();
}

function getfeedback(callback) {
    console.log("Feedback Received!")
    callback()
}