import { useEffect, useState } from "react";
import { toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Exhibit } from "./ExhibitInterface";


const AdminTable = () => {
    const [visible, setVisible] = useState([]);
    const [data, setData] = useState<Exhibit[]>([]);
  
    useEffect(() => {
      const fetchData = async () => {
        const token = localStorage.getItem('token');

        const response = await fetch('http://localhost:8080/api/adm/', {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            },
        });

        try {
            if (response.ok) {
            console.log(response);
            const jsonData = await response.json();
            setData(jsonData);
            } else {
            toast.error('Ошибка при получении данных');
            console.error('Ошибка при получении данных', response.statusText);
            }
        } catch (error) {
            console.error('Ошибка при получении данных:', error);
            toast.error('Ошибка при получении данных');
        }
      };
      fetchData();
    }, []);

  
    const handleEdit = (index: number) => {
      // Обработчик события редактирования
      // Реализуйте логику редактирования экспоната
      console.log('Редактирование экспоната:', data[index]);
    };
  

    const handleHide = async (index: number) => {

        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://localhost:8080/api/hide_unhide/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data[index]),
            });
            if (response.ok) {
                const responseData = await response.json();
                const updatedVisible = responseData.visible;
                setVisible(updatedVisible);
                console.log(visible);
                toast.success('Экспонат удалён');
            } else {
                console.error('Ошибка при удалении экспоната:', response.statusText);
                toast.error('Ошибка при удалении экспоната');
            }
        } catch (error) {
            console.error('Ошибка при удалении экспоната:', error);
            toast.error('Ошибка при удалении экспоната');
        }
      console.log('Скрытие экспоната:', data[index]);
    //   console.log('visible was', visible);
    };

    const handleDelete = async (index: number) => {
        
        const token = localStorage.getItem('token');

        try {
          const exhibitToDelete = data[index];
          const response = await fetch('http://localhost:8080/api/delete/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(exhibitToDelete),
          });
          if (response.ok) {
            const updatedData = data.filter((_, i) => i !== index);
            setData(updatedData);
            toast.success('Экспонат удалён');
          } else {
            console.error('Ошибка при удалении экспоната:', response.statusText);
            toast.error('Ошибка при удалении экспоната');
          }
        } catch (error) {
          console.error('Ошибка при удалении экспоната:', error);
          toast.error('Ошибка при удалении экспоната');
        }
      };
    
      if (!data) {
        return <div>Loading...</div>;
      }
  
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
                    <button onClick={() => handleEdit(index)}>Редактировать</button>
                    <button onClick={() => handleHide(index)}>Скрыть</button>
                    <button onClick={() => handleDelete(index)}>Удалить</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </>
    );
  };
  
  export default AdminTable;
  