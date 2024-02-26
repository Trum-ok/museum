import AdminNavbar from '../components/AdminNavbar';
import EventsTable from '../components/EventsTable';

function Events() {
  return (
    <>
        <AdminNavbar />
        <div className="container">
            <div className="back_button">
                <a href="/admin/">&lt; назад</a>
            </div>
            <h1>История действий</h1>
            <EventsTable />
        </div>
    </>
  )
}   

export default Events