import AdminNavbar from '../components/AdminNavbar';
import AdminBackButton from '../components/AdminBackButton';
import EventsTable from '../components/EventsTable';

function Events() {
  return (
    <>
        <AdminNavbar />
        <div className="container">
            <AdminBackButton />
            <h1>История действий</h1>
            <EventsTable />
        </div>
    </>
  )
}   

export default Events