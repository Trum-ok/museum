import AdminNavbar from "../components/AdminNavbar"
import AdminBackButton from '../components/AdminBackButton';

function Edit() {
  return (
    <>
    <AdminNavbar />
    <div className="container">
        <AdminBackButton />
        <h1>Редактировать сайт</h1>
        <ul>
            <li><a href="/admin/edit-page/main">Главная</a></li>
            <li><a href="/admin/edit-page/contacts">Контакты</a></li>
        </ul>
    </div>
    </>
  )
}

export default Edit