const yourname = process.argv[2];

if (!yourname) {
    console.log("Please provide your name.");
} else {
    console.log(`Hello ${yourname}`);
}
