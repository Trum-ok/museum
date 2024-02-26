import { useEffect, useState } from "react"
import AdminNavbar from '../components/AdminNavbar';
import DeletedTable from "../components/DeletedTable";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function DeletedItems() {
  return (
    <>
        <ToastContainer position="bottom-right" draggable newestOnTop/>
        <AdminNavbar />
        <div className="container">
            <div className="back_button">
                <a href="/admin/">&lt; назад</a>
            </div>
            <h1>Недавно удаленные</h1>
            <DeletedTable />
        </div>
    </>
  )
}

export default DeletedItems