import { useState, useEffect } from "react";
import { useQuery, useMutation } from "react-query";
import { useParams } from "react-router-dom";

function ChatDetail() {
  const { chatId } = useParams(); // Use destructuring to extract chatId from params

  const { data: chatData, isLoading: isChatLoading, isError: isChatError } = useQuery({
    queryKey: ["chat", chatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}`)
        .then((response) => response.json())
    ),
  });

  const { data: userData, isLoading: isUserLoading, isError: isUserError } = useQuery({
    queryKey: ["chat", chatId, "users"],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}/users`)
        .then((response) => response.json())
    ),
  });

  const [newName, setNewName] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (chatData && chatData.chat) {
      setNewName(chatData.chat.name);
    }
  }, [chatData]);

  const updateChatNameMutation = useMutation(
    (newName) =>
      fetch(`http://127.0.0.1:8000/chats/${chatId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: newName }),
      }),
    {
      onSuccess: () => {
        console.log("Chat name updated successfully.");
        // Refresh the page after successful update
        window.location.reload();
      },
      onError: (error) => {
        console.error("Error updating chat name:", error);
      },
    }
  );

  const handleNameChange = (e) => {
    setNewName(e.target.value);
  };

  const handleSubmit = () => {
    updateChatNameMutation.mutate(newName);
    setIsEditing(false); // Exit edit mode after submitting
  };

  if (isChatLoading || isUserLoading) return <div>Loading...</div>;
  if (isChatError || isUserError) return <div>Error fetching data</div>;

  return (
    <div>
      <h2>Chat details</h2>
      <div>
        <p>Name: {chatData.chat.name}</p>
        <p>Owner: {chatData.chat.owner.username}</p>
        <p>All Users:</p>
        <ul>
          {userData.users.map((user) => (
            <li key={user.id}>{user.username}</li>
          ))}
        </ul>
      </div>
      {isEditing ? (
        <div>
          <input
            type="text"
            value={newName}
            onChange={handleNameChange}
          />
          <button onClick={handleSubmit}>Submit</button>
        </div>
      ) : (
        <div>
          <button onClick={() => setIsEditing(true)}>Edit Name</button>
        </div>
      )}
    </div>
  );
}

export default ChatDetail;
