import { useState, useEffect } from 'react'
import { toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface Event {
    type_: string;
    was: string;
    now: string;
    date: Date;
    admin: string;
}


function EventsTable() {
    const [data, setData] = useState<Event[]>([]);

    useEffect(() => {
      const fetchData = async () => {
        const token = localStorage.getItem('token');

        try {
            
            const response = await fetch('http://localhost:8080/api/events/', {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                },
            });
                const jsonData = await response.json();
                setData(jsonData);
            } catch (error) {
                toast.error('Ошибка при получении данных');
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
        <section className="table">
          <table>
            <thead>
              <tr>
                <th>Тип</th>
                <th>Было</th>
                <th>Стало</th>
                <th>Время</th>
                <th>Администратор</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  <td>{row.type_}</td>
                  <td>{row.was}</td>
                  <td>
                    {row.type_ === 'Add' || row.type_ === 'Edit' || row.type_ === 'Unhide' ? (
                        <a href={`/tables/item?value=${index + 1}/`}>{row.now}</a>
                    ) : (
                        row.now
                    )}
                  </td>
                  <td>{row.date.toString()}</td>
                  <td>{row.admin}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </>
  )
}

export default EventsTable