function NotFound() {
    return (
        <>
        <div className="container">
            <main>
                <h1 style={{fontSize: "7vw", margin: 0}}>404</h1>
                <h2 style={{marginBottom: "10vh"}}>Похоже, такой страницы не существует...</h2>

                <section className="previous_next">
                    <a href="/">
                        <span>&lt; Главная</span>
                    </a>
                </section>
            </main>
        </div>
        </>
    );
  }
  
  export default NotFound;
