import "../../templates/static/style1.css"
import Navbar from './components/navbar'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Home from './pages/index';
import Contacts from './pages/contacts'
import Table from './pages/table'
import Item from "./pages/item";
import NotFound from "./pages/404";

function App() {
  return (
      <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/table" element={<Table />} />
            <Route path="/contacts" element={<Contacts />}/>
            <Route path="/tables/item" element={<Item />} />
            <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
  )
}

export default App
