import { useState } from "react";
import { Link,useNavigate } from "react-router-dom";
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

function LoginLink() {
  return (
    <div className="pt-8 flex flex-row">
      <div className="text-xs mr-2">
        already have an account?
      </div>
      <Link to="/registration" className="text-xs text-yellow-300">
        login
      </Link>
    </div>
  );
}

function Registration() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const disabled = username === "" || email === "" || password === "";

  const onSubmit = (e) => {
    e.preventDefault();

    fetch(
      "http://127.0.0.1:8000/auth/registration",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      },
    ).then((response) => {
      if (response.ok) {
        navigate("/login");
      } else if (response.status === 422) {
        response.json().then((data) => {
          setError(data.detail.entity_field + " already taken");
        });
      } else {
        setError("error logging in");
      }
    });
  }

  return (
    <div className="max-w-96 mx-auto py-8 px-4">
      <form onSubmit={onSubmit}>
        <FormInput type="text" name="username" setter={setUsername} required />
        <FormInput type="email" name="email" setter={setEmail} required/>
        <FormInput type="password" name="password" setter={setPassword} required/>
        <Button className='w-full' type='submit' disabled={disabled} >
        create account </Button>
        <Error message={error} />
      </form>
      <LoginLink />
    </div>
  );
}

export default Registration;