import ChatWindow from "../components/ChatWindow";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";


function  Dashboard()
{
    return (
        <div style={{display: 'flex' , height: '100vh'}} >
            <Sidebar />
            <div style={{flex: 1 ,display: 'flex' , flexDirection:'column' , background: '0a0e1a'}}>
               <Topbar />
               <ChatWindow />
                {/* <div style={{ flex: 1 }}></div> */}
            </div>
        </div>
    )
}

export default Dashboard