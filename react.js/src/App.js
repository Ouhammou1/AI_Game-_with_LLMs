import logo from './logo.svg';
import './App.css';
import Article from "./Article"



function App() {

  const firstArticle = `Test text, 
  often referred to as placeholder `

  const secondArticle = "to focus on the overall text, is content used to fill in gaps during the design and development phases of a project. Its primary purpose is to provide a visual representation of how the final content will look in a layout, allowing designers and developers .design without being distracted by the actual content"
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
        </a>
        <Article 
        content={firstArticle}  
        name="brahim"  
        email="barhim@gmail.com" 
        age="24">

        <h1>Hello World</h1>
        </Article>
        
        
        
        
        <Article name="brahim"  email="barhim@gmail.com" age="24" />
        <Article name="brahim"  email="barhim@gmail.com" age="24" />


      </header>
    </div>
  );
}

export default App;
