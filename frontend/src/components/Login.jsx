import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";
import FormInput from "./FormInput";
import Button from "./Button";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function RegistrationLink() {
  return (
    <div className="pt-8 flex flex-row">
      <div className="text-xs mr-2">
        don't have an account?
      </div>
      <Link to="/registration" className="text-xs text-yellow-300">
        create an account
      </Link>
    </div>
  );
}


function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");


  const navigate = useNavigate();

  const { login } = useAuth();

  const disabled = username === "" || password === "";

  const onSubmit = (e) => {
    e.preventDefault();

    fetch(
      "http://127.0.0.1:8000/auth/token",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ username, password }),
      },
    ).then((response) => {
      if (response.ok) {
        response.json().then(login);
        navigate("/chats");
      } else if (response.status === 401) {
        response.json().then((data) => {
          setError(data.detail.error_description);
        });
      } else {
        setError("error logging in");
      }
    });
  }

  return (
    <div className="max-w-96 mx-auto py-8 px-4">

    <form  onSubmit={onSubmit}>
      <FormInput type="text" name="username" setter={setUsername} required/>
      <FormInput type="password" name="password" setter={setPassword} required/>
      <Button type='submit'  disabled={disabled} >
      login </Button>
      <Error message={error} />
      </form>
      <RegistrationLink />
    </div>
  );
}

export default Login;