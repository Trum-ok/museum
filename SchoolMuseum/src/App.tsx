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

function App() {
  return (
      <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/table" element={<Table />} />
            <Route path="/contacts" element={<Contacts />}/>
        </Routes>
      </Router>
  )
}

export default App
