function Contacts() {
    return (
        <>
        <main>
            <section className="contact-section">
                <h1>Контакты</h1>
                <div className="contacts">
                    <div className="text_div">
                    <p><b>Адресс:</b> ул. 1-я Крестьянская, 14, Мытищи, Московская обл., 141014</p>
                    <p><b>Контактный телефон:</b> 7(xxx)xxx xx xx</p>
                    <p><b>e-mail:</b> somemail@mail.ru</p>
                    <h2>Режим работы:</h2>
                        &nbsp;&nbsp;&nbsp;&nbsp;<b>пн:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>вт:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>ср:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>чт:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>пт:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>сб:</b> xx:xx - xx:xx
                        <br />&nbsp;&nbsp;&nbsp;&nbsp;<b>вс:</b> xx:xx - xx:xx
                    <p />
                    </div>
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d279.6706167773242!2d37.71882571769209!3d55.89103002446313!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b5316c13d0ec4d%3A0x5f327e1cdc9b40de!2z0KHRgNC10LTQvdGP0Y8g0L7QsdGJ0LXQvtCx0YDQsNC30L7QstCw0YLQtdC70YzQvdCw0Y8g0YjQutC-0LvQsCDihJYgNQ!5e0!3m2!1sru!2sru!4v1681766947883!5m2!1sru!2sru" width="600" height="450" style={{ border: 0}} loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
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
        </>
    );
  }
  
  export default Contacts;
