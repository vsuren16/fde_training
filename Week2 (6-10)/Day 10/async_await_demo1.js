//==================
//async-awaitdemo.js
//=================
function preparePizza() {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("Pizza is ready!");
      resolve();
    }, 3000);
  });
}

function notifyCustomer() {
  return new Promise((resolve) => {
    console.log("Notifying customer...");
    resolve();
  });
}

function deliverPizza() {
  return new Promise((resolve) => {
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

async function processOrder() {
  await preparePizza();
  await notifyCustomer();
  await deliverPizza();
  await askForFeedback();
}

processOrder();
