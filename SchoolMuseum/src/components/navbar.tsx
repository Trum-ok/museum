import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="main-nav">
      <div className="logo-container">
        <a href="/">
          <img src="/logo_mus.png" alt="Наша Перловка" />
        </a>
      </div>
      <div className="default_menu">
        <ul>
          <li><NavLink to="/">ГЛАВНАЯ</NavLink></li>
          <li><NavLink to="/table/">ТАБЛИЦА</NavLink></li>
          <li><NavLink to="/contacts/">КОНТАКТЫ</NavLink></li>
        </ul>
      </div>
      <div className="toggle">
        <label className="burger">
          <span></span>
          <span></span>
          <span></span>
        </label>
      </div>
    </nav>
  );
}

export default Navbar;
