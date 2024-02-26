import { useState, useEffect } from 'react'
import { toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Exhibit } from "./ExhibitInterface";


function DeletedTable() {

    const [data, setData] = useState<Exhibit[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('token');

            try {
                const response = await fetch('http://localhost:8080/api/deleted_exhibits/', {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                },
            });
                const jsonData = await response.json();
                setData(jsonData.reverse());
            } catch (error) {
                toast.error('Ошибка при получении данных');
                console.error('Ошибка при получении данных:', error);
            }
        };
        fetchData();
    }, []);

    const handleRestore = async (index: number) => {
        try {
            const token = localStorage.getItem('token');
            console.log(data[index])
      
            const response = await fetch('http://localhost:8080/api/restore/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
              },
              body: JSON.stringify(data[index]),
            });
      
            if (response.ok) {
                toast.success('Экспонат восстановлен');
                console.log('Восстановление экспоната:', data[index]);
            } else {
                toast.error('Ошибка при восстановлении экспоната');
                console.error('Error restoring exhibit:', response.statusText);
            }
        } catch (error) {
            toast.error('Ошибка при восстановлении экспоната');
            console.error('Error restoring exhibit:', error);
        }
      };

    if (!data) {
        return <div>Loading...</div>;
    }

    console.log(data)

  return (
    <>
        <section className="table">
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
                <th>Действия</th>
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
                  <td>
                    {<button onClick={() => handleRestore(index)}>Восстановить</button>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </>
  )
}

export default DeletedTable