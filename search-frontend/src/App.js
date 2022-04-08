import './App.css';
import Navbar from 'react-bootstrap/Navbar'
import Container from 'react-bootstrap/Container'
import Search from './search.js'

function App() {
  document.title = "Academic Search"
  return (
    <div className="App">
      <header>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand href="#home">
              Paper Search Powered by NLP
            </Navbar.Brand>
          </Container>
        </Navbar>
      </header>
      <br />
      <Search/>
    </div>
  );
}

export default App;
