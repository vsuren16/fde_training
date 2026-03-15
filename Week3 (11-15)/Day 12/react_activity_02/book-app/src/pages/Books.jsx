import { useState } from "react";
import { initialBooks } from "../data/books";

function Books() {
  const [books, setBooks] = useState(initialBooks);
  const [currentPage, setCurrentPage] = useState(1);
  const [bookName, setBookName] = useState("");

  const booksPerPage = 5;
  const start = (currentPage - 1) * booksPerPage;
  const pageBooks = books.slice(start, start + booksPerPage);

  function addBook() {
    if (!bookName) return;
    setBooks([...books, {
      id: books.length + 1,
      name: bookName,
      price: 500,
      publisher: "New Publisher"
    }]);
    setBookName("");
  }

  function deleteBook(id) {
    setBooks(books.filter(b => b.id !== id));
  }

  return (
    <>
      <h3>Books</h3>

      <div className="mb-3">
        <input className="form-control mb-2"
          placeholder="Book Name"
          value={bookName}
          onChange={(e) => setBookName(e.target.value)} />
        <button className="btn btn-success" onClick={addBook}>AddBook</button>
    </div>

      <table className="table table-bordered">
        <thead className="table-dark">
          <tr>
            <th>Select</th>
            <th>Name</th>
            <th>Price</th>
            <th>Publisher</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {pageBooks.map(book => (
            <tr key={book.id}>
              <td><input type="checkbox" /></td>
              <td>{book.name}</td>
              <td>{book.price}</td>
              <td>{book.publisher}</td>
              <td>
                <button className="btn btn-danger btn-sm"
                  onClick={() => deleteBook(book.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button className="btn btn-secondary me-2"
        disabled={currentPage === 1}
        onClick={() => setCurrentPage(currentPage - 1)}>Prev</button>

      <button className="btn btn-secondary"
        disabled={start + booksPerPage >= books.length}
        onClick={() => setCurrentPage(currentPage + 1)}>Next</button>
    </>
  );
}

export default Books;