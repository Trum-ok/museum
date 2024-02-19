import { useEffect, useState } from "react";

interface Exhibit {
    name: string;
    quantity: number;
    obtaining: string;
    discovery: string;
    description: string;
    assignment: string;
    inventory_number: {
      number: number;
      collection: string;
      fund: string;
    };
}

const Table = () => {
  const [data, setData] = useState<Exhibit[]>([]);

  useEffect(() => {
    // Метод для получения данных из API
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/exhibits');
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    };
    fetchData();
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
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
                    {/* <a href={`http://localhost:8080/api/item?value=${index + 1}/`}>{row.name}</a> */}
                    <a href={`/tables/item?value=${index + 1}/`}>{row.name}</a>
                  </td>
                  <td>{row.quantity}</td>
                  <td>{row.obtaining}</td>
                  <td>{row.discovery}</td>
                  <td>{row.description}</td>
                  <td>{row.assignment}</td>
                  <td>{`${row.inventory_number.number}/${row.inventory_number.collection}/${row.inventory_number.fund}`}</td>
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
    </div>
  );
};

export default Table;
