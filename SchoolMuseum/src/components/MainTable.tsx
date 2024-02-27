import { useEffect, useState } from "react";
import { Exhibit } from "../components/ExhibitInterface";

function MainTable() {

    const [data, setData] = useState<Exhibit[]>([]);

    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://localhost:8080/api/exhibits');
          const jsonData = await response.json();
          const sortedData = jsonData.sort((a: Exhibit, b: Exhibit) => a.inventory_number.number - b.inventory_number.number);
          setData(sortedData);
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
    <>
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
    </>
    )
}

export default MainTable