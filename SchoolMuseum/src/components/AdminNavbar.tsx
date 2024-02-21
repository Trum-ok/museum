import { NavLink, useNavigate } from 'react-router-dom';
import Pic from "../assets/img/logo_mus.png";

function AdminNavbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };


  return (
    <>
        <nav className='main-nav'>
        <ul>
            <li><NavLink to="/"><img src={Pic} alt="logo" style={{width: 40, height: 40}}/></NavLink></li>
            <li><button onClick={handleLogout}>Выход</button></li>
        </ul>
    </nav>
    </>
  )
}

export default AdminNavbar