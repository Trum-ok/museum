import Navbar from "../components/navbar";
import { useState, useEffect } from 'react';
import 'react-toastify/dist/ReactToastify.css';

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

function Contacts() {
    const [contactInfo, setContactInfo] = useState<Info>();

    useEffect(() => {
        const fetchContactInfo = async () => {
            try {
                const response = await fetch('http://localhost:8080/api/contacts/');
                if (response.ok) {
                    const data = await response.json();
                    console.log(data)
                    setContactInfo(data);
                }
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        };
        fetchContactInfo();
    }, []);

    return (
        <>
            <Navbar />
            <div className="container">
                <main>
                    <section className="contact-section">
                        <h1>Контакты</h1>
                        <div className="contacts">
                            <div className="text_div">
                                {contactInfo && (
                                    <>
                                        <p><b>Адрес:</b> {contactInfo.address}</p>
                                        <p><b>Контактный телефон:</b> {contactInfo.phone}</p>
                                        <p><b>e-mail:</b> {contactInfo.email}</p>
                                        <h2>Режим работы:</h2>
                                        <p><b>Пн:</b> {contactInfo.hours.mon}</p>
                                        <p><b>Вт:</b> {contactInfo.hours.tue}</p>
                                        <p><b>Ср:</b> {contactInfo.hours.wed}</p>
                                        <p><b>Чт:</b> {contactInfo.hours.thu}</p>
                                        <p><b>Пт:</b> {contactInfo.hours.fri}</p>
                                        <p><b>Сб:</b> {contactInfo.hours.sat}</p>
                                        <p><b>Вс:</b> {contactInfo.hours.sun}</p>
                                    </>
                                )}
                            </div>
                            {contactInfo && (
                                <iframe src={contactInfo.map} width="600" height="450" style={{ border: 0 }} loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
                            )}
                        </div>
                    </section>
                    <section className="previous_next">
                        <a href="/table/">
                            <span>&lt; Таблица </span>
                        </a>
                        <a href="/">
                            <span>Главная &gt;</span>
                        </a>
                    </section>
                </main>
            </div>
        </>
    );
}

export default Contacts;
