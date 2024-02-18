import sl1 from "../assets/img/sl1.webp"
import sl2 from "../assets/img/sl2.webp"
import sl3 from "../assets/img/sl3.webp"
import sl4 from "../assets/img/sl4.webp"
import sl5 from "../assets/img/sl5.webp"
import sl6 from "../assets/img/sl6.webp"
import sl7 from "../assets/img/sl7.webp"
import sl8 from "../assets/img/sl8.webp"

function Home() {
    return (
        <>
        <div className="container">
        <main>
            <section className="about_museum">
                <h1>Музей</h1>
                <h2>"Наша Перловка"</h2>
                <div className="about_museum">
                    <p className="about_text">
                            &nbsp;&nbsp;&nbsp;&nbsp;Школьный музей "Наша Перловка" расположен в МБОУ СОШ №10 (бывшей МБОУ СОШ №5) в г.о. Мытищи, в Московской области. Музей открыт 10 декабря 2009 г. на месте школьной библиотеки. Он является местом, где учащиеся могут познакомиться с историей своего Мытищ, школы, а также с местными традициями и достижениями.
                            <br /><br />&nbsp;&nbsp;&nbsp;&nbsp;Музей "Наша Перловка" содержит экспозиции, посвященные разным периодам истории города Мытищи («Перловка и ее жители», «История Донской церкви», «Перловка во время ВОВ», «История образования в Перловке»). В экспозициях представлены различные артефакты, фотографии, документы и другие материалы, связанные с историей города, его жителями, а также с историей школы №5.
                            <br /><br />&nbsp;&nbsp;&nbsp;&nbsp;В музее также проводятся различные образовательные программы и мероприятия, такие как лекции, экскурсии, мастер-классы, конкурсы и выставки. Они позволяют учащимся расширить свои знания о истории родного города, развивать интерес к историческому наследию и патриотическому воспитанию.
                            <br /><br />&nbsp;&nbsp;&nbsp;&nbsp;Школьный музей "Наша Перловка" является важным культурным и образовательным центром для учащихся и педагогов школы, а также для местных жителей и гостей города Мытищи. Он способствует сохранению и продвижению исторического наследия города и его учреждений, а также развитию интереса к истории и культуре среди молодого поколения.
                    </p>
                    <img src="../static/img/main_fr_1.webp" alt="" />
                </div>
            </section>
            {/* <hr style={{border: "2px", color: "#AB6C3C"}} /> */}
            <section className="slider_section">
                <div id="image-track" data-mouse-down-at="0" data-prev-percentage="0">
                <img className="image" src={sl1} draggable="false" />
                <img className="image" src={sl2} draggable="false" />
                <img className="image" src={sl3} draggable="false" />
                <img className="image" src={sl4} draggable="false" />
                <img className="image" src={sl5} draggable="false" />
                <img className="image" src={sl6} draggable="false" />
                <img className="image" src={sl7} draggable="false" />
                <img className="image" src={sl8} draggable="false" />
                </div>
            </section>
            <section className="previous_next">
                <a href="/contacts/"> 
                    <span>&lt; Контакты</span>
                </a>
                <a href="/table/">
                    <span>Таблица &gt;</span>
                </a>
            </section>
        </main>
        <script src="../static/slider.js"></script>
        </div>
        </>
    );
  }
  
  export default Home;
