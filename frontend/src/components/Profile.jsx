import { useEffect, useState } from "react";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [createdAt, setCreatedAt] = useState("");
  const [readOnly, setReadOnly] = useState(true);

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
      const createdAtDate = new Date(user.created_at);
      const formattedCreatedAt = createdAtDate.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
      setCreatedAt(formattedCreatedAt);
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("username: " + username);
    console.log("email: " + email);
    console.log("createdAt: " + createdAt);
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (

    <div className="max-w-96 mx-auto px-4 py-8">
    <form onSubmit={onSubmit}>
      <table className="w-full border rounded px-4 py-2 my-4">
        <thead>
          <tr className="border ">
            <th className="text-2xl font-bold px-4 py-2 text-left">details</th>
          </tr>
        </thead>
        <tbody>
          <tr className="border">
            <td className="text-left px-4 text-gray-400 font-semibold">username</td>
            <td className="text-right ">
              <FormInput
                name="username"
                type="text"
                value={username}
                readOnly={readOnly}
                setter={setUsername}
              />
            </td>
          </tr>
          <tr className="border ">
            <td className="text-left px-4 text-gray-400 font-semibold">email</td>
            <td className="text-right ">
              <FormInput
                name="email"
                type="email"
                value={email}
                readOnly={readOnly}
                setter={setEmail}
              />
            </td>
          </tr>
          <tr className="border">
            <td className="text-left px-4 text-gray-400 font-semibold">member Since</td>
            <td className="text-right">
              <FormInput
                name="member since"
                type="text"
                value={createdAt}
                readOnly={readOnly}
                setter={setCreatedAt}
              />
            </td>
          </tr>
        </tbody>
      </table>
       
    <Button onClick={logout}>
      logout
        </Button>
        </form>
    </div>
  );
}

export default Profile;