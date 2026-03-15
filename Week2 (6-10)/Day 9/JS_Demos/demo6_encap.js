class Person {
    #firstname
    #lastname

get fullname() {
    return this.firstname + " " + this.lastname;
}

set fullname(name) {
    const parts = name.split(" ");
    this.#firstname = parts[0];
    this.#lastname = parts[1];
 }
}

let p1 = new Person();
console.log(p1.fullname = ('abc tyr'))
console.log(p1.firstname )
console.log(p1.lastname )