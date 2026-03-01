import logo from './logo.svg';
import './App.css';
import Header from "./Header"
import Post  from './Post';
import SideMenu  from './SideMenu';
import "./TagButtonStyle.css"


function App() {
  return (
    <div className="App">
      <Header/>
      <div style={{display: "flex" , justifyContent: "center"}} >

        <div  style={{display: "flex" , with: "60%"}}>

          <div style={{width:"70%"}}>
            <Post />
            <Post />
            <Post />
            <Post />
          </div>

          <div style={{width: "30%"}}>
            <SideMenu />
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
