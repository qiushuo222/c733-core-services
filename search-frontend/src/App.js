import './App.css';
import Navbar from 'react-bootstrap/Navbar'
import Container from 'react-bootstrap/Container'
import Search from './search.js'

function App() {
  return (
    <div className="App">
      <header>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand href="#home">
              Fancy Search
            </Navbar.Brand>
          </Container>
        </Navbar>
      </header>
      <Search/>
    </div>
  );
}

export default App;
