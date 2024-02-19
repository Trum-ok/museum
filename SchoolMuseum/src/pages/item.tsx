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

function Item() {
    const [exhibit, setExhibit] = useState<Exhibit | null>(null);
    const [value, setValue] = useState<string>("");

    useEffect(() => {
        const fetchExhibit = async () => {
            try {
                const searchParams = new URLSearchParams(window.location.search);
                const valueParam = searchParams.get("value");
                setValue(valueParam || "");
                const response = await fetch(`http://localhost:8080/api/item/?value=${valueParam}`);
                if (!response.ok) {
                    throw new Error('Ошибка при получении данных');
                }
                const jsonData = await response.json();
                setExhibit(jsonData);
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        };
        fetchExhibit();
    }, []);

    if (!exhibit) {
        return (
        <>
            <div className="container">
                <main>
                    <div className="back_button">
                        <a href="/table/">&lt; назад</a>
                    </div>
                    <div style={{marginTop: "5vh"}}>Loading...</div>
                </main>
            </div>
        </>);
    }
    
    return (
            <>
            <div className="container">
                <main>
                    <div className="back_button">
                        <a href="/table/">&lt; назад</a>
                    </div>
                    <div className="exhibit-view">
                        <div className="exhibit">
                            <h1>{exhibit.name}</h1>
                            <section className="example_exhib">
                                <div className="example_exhib_text">
                                    <p><b>Кол-во:</b> {exhibit.quantity} шт</p>
                                    <p><b>Способ получения:</b> {exhibit.obtaining}</p>
                                    <p><b>Место обнаружения:</b> {exhibit.discovery}</p>
                                    <p><b>Описание:</b> {exhibit.description}</p>
                                    <p><b>Назначение:</b> {exhibit.assignment}</p>
                                    <p><b>Инвентарный №:</b> {exhibit.inventory_number.number}/{exhibit.inventory_number.collection}/{exhibit.inventory_number.fund}</p>
                                </div>
                            </section>
                        </div>
                        <img src="" alt="exhibit-image" />
                    </div>
                    <section className="previous_next" id="previous_next_item">
                        <a href={`item?value=${parseInt(value) - 1}/`}>
                            <span>&lt; Предыдущий</span>
                        </a>
                        <a href={`item?value=${parseInt(value) + 1}/`}>
                            <span>Следующий &gt;</span>
                        </a>
                    </section>
                </main>
            </div>
            </>
  )
}

export default Item;