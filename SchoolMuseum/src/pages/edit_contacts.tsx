import { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AdminBackButton from '../components/AdminBackButton';

interface Hours {
    mon: string;
    tue: string;
    wed: string;
    thu: string;
    fri: string;
    sat: string;
    sun: string;
}

interface Info {
    address: string;
    phone: string;
    email: string;
    hours: Hours;
    map: string;
}

function EditContactsPage() {

    const defaultContactInfo: Info = {
        address: '',
        phone: '',
        email: '',
        hours: {
            mon: '',
            tue: '',
            wed: '',
            thu: '',
            fri: '',
            sat: '',
            sun: '',
        },
        map: '',
    };

    const [contactInfo, setContactInfo] = useState<Info>(defaultContactInfo);

    useEffect(() => {
        const fetchContactInfo = async () => {
            try {
                const response = await fetch('http://localhost:8080/api/contacts/');
                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    setContactInfo(data);
                }
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        };
        fetchContactInfo();
    }, []);

  // Обработчик изменения данных в форме
  const handleChange = (e) => {
    const { name, value } = e.target;
    // Если изменяемое поле является частью объекта hours, обновляем его вложенное значение
    if (name.startsWith('hours')) {
        const day = name.split('_')[1];
        setContactInfo(prevState => ({
            ...prevState,
            hours: {
                ...prevState.hours,
                [day]: value
            }
        }));
    } else {
        // Иначе обновляем другие поля
        setContactInfo(prevState => ({
            ...prevState,
            [name]: value
        }));
    }
  };

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('token');

    try {
        const response = await fetch('http://localhost:8080/api/edit_pages/contacts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(contactInfo), // Отправляем данные формы
        });
        if (response.ok) {
            setTimeout(() => {
                console.log("success")
                toast.success("Изменения сохранены. Вы будете перенаправлены через 5 секунд")
                // Перенаправление на другую страницу через 5 секунд
                // setTimeout(() => {
                //     // Здесь указываете путь к другой странице
                //     window.location.href = '/other-page';
                // }, 5000);
            }, 5000);
        } else {
            console.error('Ошибка при сохранении данных:', response.statusText);
            toast.error('Ошибка при сохранении данных');
        }
    } catch (error) {
        toast.error("Ошибка при сохранении данных")
        console.error('Ошибка при сохранении данных:', error);
    }
  };

  return (
    <>
        <ToastContainer position="bottom-right" draggable newestOnTop/>
        <div className="container">
            <AdminBackButton />
            <h1>Редактирование страницы контактов</h1>
            <div className="ContactsForm">
                <form onSubmit={handleSubmit}>
                    <label>
                        Адрес:
                        <input
                        type="text"
                        name="address"
                        value={contactInfo.address}
                        onChange={handleChange}
                        />
                    </label>
                    <br />
                    <label>
                        Контактный телефон:
                        <input
                        type="text"
                        name="phone"
                        value={contactInfo.phone}
                        onChange={handleChange}
                        />
                    </label>
                    <br />
                    <label>
                        E-mail:
                        <input
                        type="text"
                        name="email"
                        value={contactInfo.email}
                        onChange={handleChange}
                        />
                    </label>
                    <br />
                    <div className="hours">
                        <label>
                            Режим работы:
                        </label>
                        <br />
                        <label>
                            Понедельник:
                            <input
                            type="text"
                            name="hours_mon"
                            value={contactInfo.hours.mon}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Вторник:
                            <input
                            type="text"
                            name="hours_tue"
                            value={contactInfo.hours.tue}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Среда:
                            <input
                            type="text"
                            name="hours_wed"
                            value={contactInfo.hours.wed}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Четверг:
                            <input
                            type="text"
                            name="hours_thu"
                            value={contactInfo.hours.thu}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Пятница:
                            <input
                            type="text"
                            name="hours_fri"
                            value={contactInfo.hours.fri}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Суббота:
                            <input
                            type="text"
                            name="hours_sat"
                            value={contactInfo.hours.sat}
                            onChange={handleChange}
                            />
                        </label>
                        <br />
                        <label>
                            Воскресенье:
                            <input
                            type="text"
                            name="hours_sun"
                            value={contactInfo.hours.sun}
                            onChange={handleChange}
                            />
                        </label>
                    </div>
                    <br />
                    <label>
                        Ссылка на карту:
                        <input
                        type="text"
                        name="map"
                        value={contactInfo.map}
                        onChange={handleChange}
                        />
                    </label>
                    <br />
                    <button type="submit">Сохранить</button>
                </form>
            </div>
        </div>
    </>
  );
}

export default EditContactsPage;
