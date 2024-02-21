import { NavLink, useNavigate } from 'react-router-dom';

function AdminNavbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };


  return (
    <>
        <nav className='main-nav'>
        <div className="logo-container">
          <a href="/">
            <img src="/logo_mus.png" alt="Наша Перловка" />
          </a>
        </div>
        <ul>
            <li><button onClick={handleLogout}>Выход</button></li>
            <li><NavLink to="/admin/add">Добавить</NavLink></li>
            {/* <li><NavLink to="/admin/add">Р</NavLink></li> */}
        </ul>
    </nav>
    </>
  )
}

export default AdminNavbar