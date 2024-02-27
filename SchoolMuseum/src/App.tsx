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
import DeletedItems from "./pages/deleted_items";
import Events from "./pages/events";
import Edit from "./pages/edit";
import EditContactsPage from "./pages/edit_contacts";
import EditMainPage from "./pages/edit_main";
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
                <Route path="/admin/recently-deleted" element={<DeletedItems />}/>
                <Route path="/admin/events" element={<Events />}/>
                <Route path="/admin/edit-page" element={<Edit />}/>
                <Route path="/admin/edit-page/contacts" element={<EditContactsPage />}/>
                <Route path="/admin/edit-page/main" element={<EditMainPage />}/>
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
