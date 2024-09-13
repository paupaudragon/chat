import { QueryClient, QueryClientProvider } from 'react-query';
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider } from "./context/user";

import { BrowserRouter, Navigate, Routes, Route, Link } from 'react-router-dom';
import Chats from './components/Chats'
import Login from "./components/Login";
import TopNav from "./components/TopNav";
import Profile from "./components/Profile";
import Registration from "./components/Registration";
import ChatDetail from "./components/ChatDetail";


const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
        <div className='text-center'>
          logged in: {isLoggedIn.toString()}
          This is pony express chat. 
        </div>
      <button className="bg-zinc-700 border rounded px-2 py-2 my-5 hover:bg-zinc-600">
        <Link to="/chats">Get started</Link>
      </button>
      </div>   
  );
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chats" element={<Chats />} />
      <Route path="/chats/:chatId/details" element={<ChatDetail />} />
      <Route path="/chats/:chatId" element={<Chats />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="*" element={<Navigate to="/chats" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
} 


function Main() {
  const { isLoggedIn } = useAuth()
  // console.log("isLoggedIn:", isLoggedIn.toString());
  return (
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />}
    </main>
  );
}

function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-zinc-700 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            {/* <ChatProvider> */}
              <div className={className}>
                <Header />
                <Main />
              </div>
            {/* </ChatProvider> */}
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App
