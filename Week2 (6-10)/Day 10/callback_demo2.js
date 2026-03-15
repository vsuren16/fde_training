// //1 basic Promise demo
// function preparePizza() {
//     return new Promise((resolve,reject) => {
//         const ready = true; 
//         if (ready) {
//             resolve("Pizza is ready!");
//         } else {
//             reject("Pizza got burned.");
//         }
//     });
// }

// preparePizza()
//     .then(msg => console.log("Succss:",msg))
//     .catch(err => console.log("Error log"))

//2 basic Promise demo
// function preparePizza() {
//     return new Promise((resolve,reject) => {
//         const ready = true; 
//         setTimeout(() => {
//         if (ready) {
//             resolve("Pizza is ready!");
//         } else {
//             reject("Pizza got burned.");
//         }
//     },3000);
// });
// }

function preparePizza() {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("Pizza is ready!");
      resolve();
    }, 3000);
  });
}


function notifyCustomer() { 
    return new Promise((resolve,reject) => {
        console.log("Notifying customer...")
        resolve();
});}


function deliverPizza() {
  return new Promise((resolve,reject) => {
    setTimeout(() => {
      console.log("Pizza delivered!");
      resolve();
    }, 2000);
  });
}

function askForFeedback() {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("Customer says: 'Delicious!'");
      resolve();
    }, 1000);
  });
}

preparePizza()
  .then(notifyCustomer)
  .then(deliverPizza)
  .then(askForFeedback);
