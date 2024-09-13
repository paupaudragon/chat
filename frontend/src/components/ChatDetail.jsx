import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import FormInput from "./FormInput";
import Button from "./Button";

function ChatDetail() {
  const { chatId } = useParams();
  const { token } = useAuth();
  const [chatData, setChatData] = useState(null);
  const [userData, setUserData] = useState([]);
  const [newChatName, setNewChatName] = useState("");
  const [error, setError] = useState(null);
  const [allUsers, setAllUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState("");
  const [isUserAdded, setIsUserAdded] = useState(false); // Flag to track if user is added

  useEffect(() => {
    // Fetch chat details
    fetchChatDetails();
  }, [chatId, token]); // Fetch chat details only when chatId or token changes

  useEffect(() => {
    // Fetch users of this chat
    fetchUsersOfChat();
  }, [chatId, token, isUserAdded]); // Fetch users when chatId, token, or isUserAdded flag changes

  useEffect(() => {
    // Fetch all users
    fetchAllUsers();
  }, [token]); // Fetch all users only when token changes

  const fetchChatDetails = () => {
    fetch(`http://127.0.0.1:8000/chats/${chatId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setChatData(data))
      .catch((error) => setError(error.message));
  };

  const fetchUsersOfChat = () => {
    fetch(`http://127.0.0.1:8000/chats/${chatId}/users`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setUserData(data.users))
      .catch((error) => setError(error.message));
  };

  // Inside the useEffect that fetches all users
const fetchAllUsers = () => {
  fetch(`http://127.0.0.1:8000/users`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const ownerUserId = chatData?.chat?.owner?.id;
      const chatUserIds = userData.map((user) => user.id);
      // Filter out users who are the owner or already in the chat
      const filteredUsers = data.users.filter((user) => user.id !== ownerUserId && !chatUserIds.includes(user.id));
      setAllUsers(filteredUsers);
    })
    .catch((error) => setError(error.message));
};


  const handleUpdateChatName = (e) => {
    e.preventDefault();
    fetch(`http://127.0.0.1:8000/chats/${chatId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: newChatName }),
    })
      .then((response) => {
        if (response.ok) {
          setChatData({ ...chatData, chat: { ...chatData.chat, name: newChatName } });
          setNewChatName("");
        } else {
          throw new Error("Failed to update chat name");
        }
      })
      .catch((error) => setError(error.message));
  };

  const handleRemoveUser = (userId) => {
    fetch(`http://127.0.0.1:8000/chats/${chatId}/users/${userId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setUserData(data.users))
      .catch((error) => setError(error.message));
  };

  const handleAddUser = () => {
    if (selectedUserId) {
      fetch(`http://127.0.0.1:8000/chats/${chatId}/users/${selectedUserId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setUserData(data.users);
          setIsUserAdded(true); // Set flag to true after user is added
        })
        .catch((error) => setError(error.message));
    }
  };

  useEffect(() => {
    if (isUserAdded) {
      setIsUserAdded(false); // Reset flag after user is added
    }
  }, [isUserAdded]); // Reset flag when isUserAdded changes

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!chatData || !userData) {
    return <div>Loading...</div>;
  }

  const user = useUser();
  const isOwner = user.id === chatData?.chat?.owner?.id;

  return (
    <div className="max-w-96 mx-auto py-8 px-4">
      <h1>Chat Details</h1>
      <p>Chat Name: {chatData.chat.name}</p>
      <p>Owner: {chatData.chat.owner.username}</p>
      <p>Users:</p>
      <ul>
        {userData.map((user) => (
          <li key={user.id}>
            {user.username}
            {isOwner && <Button onClick={() => handleRemoveUser(user.id)}>Remove</Button>}
          </li>
        ))}
      </ul>
      <form onSubmit={handleUpdateChatName}>
        <FormInput
          type="text"
          name="newChatName"
          value={newChatName}
          setter={setNewChatName}
          placeholder="Enter new chat name"
          required
          disabled={!isOwner}
        />
        <Button type="submit" disabled={!isOwner}>Update Chat Name</Button>
      </form>
      <select value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)} disabled={!isOwner}>
        <option value="">Select User to Add</option>
        {allUsers.map((user) => (
          <option key={user.id} value={user.id}>
            {user.username}
          </option>
        ))}
      </select>
      <Button onClick={handleAddUser} disabled={!isOwner}>Add User</Button>
    </div>
  );
  
}

export default ChatDetail;
