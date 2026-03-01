import logo from './logo.svg';
import './App.css';
import Header from "./Header"
import Post  from './Post';

function App() {
  return (
    <div className="App">
      <Header/>

      <div style={{width:"50%"}}>
        <Post />
      </div>
      
    </div>
  );
}

export default App;
