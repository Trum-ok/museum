import { useEffect, useState } from "react"

interface Exhibit {
    // Define the structure of your exhibit data
    // This should match the structure returned by your Flask endpoint
    // Adjust the types according to your data structure
    id: number;
    name: string;
    quantity: number;
    // Add more properties as needed
  }

function Table() {
    const [data, setData] = useState<Exhibit[]>([]);

    useEffect(() => {
      fetch("/table") // Update the URL accordingly if needed
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.error("Error fetching data:", error));
    }, []);

  return (
    <main>
      <section className="table">
        <h1>Электронная</h1>
        <h2>книга поступлений</h2>
        <table>
          <thead>
            <tr>
              <th>Название</th>
              <th>Кол-во</th>
              <th>Способ получения</th>
              <th>Место обнаружения</th>
              <th>Описание</th>
              <th>Назначение</th>
              <th>Инв. №</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>
                  <a href={`/item?value=${index}/`}>{row[0]}</a>
                </td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
                <td>{`${row[6]}/${row[7]}/${row[8]}`}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="previous_next">
        <a href="/contacts/">
          <span>&lt; Контакты</span>
        </a>
        <a href="/">
          <span>Главная &gt;</span>
        </a>
      </section>
    </main>
  );
}

export default Table;
