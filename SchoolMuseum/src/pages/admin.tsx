import AdminNavbar from '../components/AdminNavbar';
import AdminTable from '../components/AdminTable';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Admin() {
  return (
    <>
    <ToastContainer position="bottom-right" draggable newestOnTop/>
    <AdminNavbar />
    <div className="container">
        <header>
            <h1>Панель управления музеем</h1>
        </header>
        <main>
            <AdminTable />
        </main>
    </div>
    </>
  )
}

export default Admin;
