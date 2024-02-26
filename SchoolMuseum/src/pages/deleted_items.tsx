import AdminNavbar from '../components/AdminNavbar';
import AdminBackButton from '../components/AdminBackButton';
import DeletedTable from "../components/DeletedTable";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function DeletedItems() {
  return (
    <>
        <ToastContainer position="bottom-right" draggable newestOnTop/>
        <AdminNavbar />
        <div className="container">
            <AdminBackButton />
            <h1>Недавно удаленные</h1>
            <DeletedTable />
        </div>
    </>
  )
}

export default DeletedItems