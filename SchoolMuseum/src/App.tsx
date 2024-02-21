import "./style.css"
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { useState, useEffect } from "react";
import Home from './pages/index';
import Contacts from './pages/contacts'
import Table from './pages/table'
import Item from "./pages/item";
import NotFound from "./pages/404";
import Login from "./pages/login";
import Admin from "./pages/admin";
import AddExhibit from "./pages/add_exhibit";
import { isAuthenticated } from './auth';

function App() {
  const [authenticated, setAuthenticated] = useState(true);

  useEffect(() => {
    const checkAuthentication = async () => {
      const auth = await isAuthenticated();
      setAuthenticated(auth);
    };

    checkAuthentication();
  }, []);

  console.log(authenticated)

  return (
      <Router>
        <Routes>  
            <Route path="/" element={<Home />} />
            <Route path="/table" element={<Table />} />
            <Route path="/contacts" element={<Contacts />}/>
            <Route path="/tables/item" element={<Item />} />
            <Route path="/login" element={<Login />} />
            {authenticated ? (
              <>
                <Route path="/admin/*" element={<Admin />} />
                <Route path="/admin/add" element={<AddExhibit />} />
              </>
            ) : (
              <Route path="/admin/*" element={<Navigate to="/login" />} />
            )}  
            <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
  )
}

export default App;
