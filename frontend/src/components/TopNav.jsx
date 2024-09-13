import { NavLink } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

function NavItem({ to, name, right }) {
  const className = [
    "border-slate-400",
    "py-2 px-4",
    "hover:bg-gray-500",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-gray-500" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}
function AuthenticatedNavItems() {
  const user = useUser()
  return (
    <>
      <NavItem to="/chats" name="poney express" />
      <div className='flex-1' />
      <NavItem to="/profile" name= {user?.username} right />
    </>
  );
}

function UnauthenticatedNavItems() {
  return (
    <>

      <NavItem to="/" name='pony express' />
      <div className='flex-1' />
      <NavItem to="/login" name='login' right />
      
    </>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="flex flex-row border-b-4 border-slate-400">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;