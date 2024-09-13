import { useQuery } from "react-query"
import { Link, useParams } from "react-router-dom"
import NewChat from "./NewChat";

const h2ClassName = "py-1 mb-2 border-2 border-white rounded text-center font-bold"
function formatDate(dateString) {
    
    const options = { weekday: 'short', month: 'short', day: '2-digit', year: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options).replace(/,/g, ''); 
    
}

function DateAndTimeConversion(dateTimeStr) {
    const dateTime = new Date(dateTimeStr);

    const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true
    };

    const formattedDateTime = dateTime.toLocaleString('en-US', options);
    const commaIndex = formattedDateTime.indexOf(", ");
    const datePart = formattedDateTime.slice(0, commaIndex + 14).replace(',', ''); 
    const timePart = formattedDateTime.slice(commaIndex + 15).replace(',', '');
    var result = datePart + ' -' + timePart
    return result.replace(',', '');
}

function ChatListItem({ chat, active }) {

    const className = [
        "flex flex-col",
        "border-2 rounded", 
        'mb-4 p-2', 
        "hover:bg-zinc-900", 
        active ? 
            "bg-zinc-800 border-orange-400" : 
            "border-green-500"
    ].join(" ")

    return (
        <Link key={chat.id} to={`/chats/${chat.id}`} className={className}>
            <div className="text-orange-400 font-extrabold" key={`${chat.id}-name`}>
                {chat.name}
            </div>
            <div className="text-xxs text-gray-400 ml-2">
                Created at: {formatDate(chat.created_at)}
            </div>
            
        </Link>
    )
}

function ChatList({ chats, chatId }) {
    return (
     
        <div className="flex  flex-col overflow-y-scroll">
            {chats.map((chat) => {
                return <ChatListItem key={chat.id} chat={chat} active={chat.id == parseInt(chatId.chatId)} />;
            })}
        </div>
    )
}


function ChatListContainer(chatId) {

    const { data, isLoading, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            fetch(
                "http://127.0.0.1:8000/chats"
            ).then((response)=>response.json())
        ),
           
    })

    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    
    if (data?.chats) { //data && data.chats
        return (
            <div className="flex flex-col max-h-fitted">
                {/* <h2 className={h2ClassName}>pony express</h2> */}
                <ChatList chats={data.chats} chatId={chatId}></ChatList>
            </div>
        )
    }
    
    return (
        <h2 className={h2ClassName}>chat list </h2>
    )
}

function Chats() {
    const {chatId }= useParams();
    // console.log(chatId)
    return (
        <div className='grid grid-cols-3 gap-5 '>
            <ChatListContainer chatId = {chatId}></ChatListContainer >
            <Messages></Messages>
        </div>
    )

}


// ===================Message related============================= 
// MessageCardContainer -> MessageCardQueryContainer -> Messages
function MessageCardContainer({ message}) {
    return (
   
        <div className="border border-violet-500 rounded my-4 px-4 py-2">
            
            <div key={message.id}>
                <div className="flex flex-row justify-between">
                    <div className="text-green-500 text-sm font-bold">{message.user.username}</div>
                    <div className="text-gray-400 text-xxs">{DateAndTimeConversion(message.created_at)}</div>
                </div>
                <div className="ml-4 ">{message.text}</div>
            </div>
        </div>
    )
    
}

function MessageCardQueryContainer({ chatId }) {

    if (!chatId) return <h2 className={h2ClassName}>select a chat</h2>
    
    const { data } = useQuery({
        queryKey: ["chat", chatId],
        queryFn: () => (
            fetch(
                `http://127.0.0.1:8000/chats/${chatId}/messages`
                ).then((response)=>response.json())
                ),
                
            })
            
            if (data?.messages) {
                return (
                <div className="border-2 border-orange-400 rounded px-2 overflow-y-scroll mb-2">
                    {data.messages.map((message) => (
                        <MessageCardContainer key={message.id} message={message} />
                    ))}
                </div>
            );
        }
}

function Messages() {
    const { chatId } = useParams()
    if (chatId) {
        return (
            <div className='col-span-2 flex flex-col max-h-fitted'>
                <MessageCardQueryContainer chatId={chatId}></MessageCardQueryContainer>
                <NewChat chatId={chatId} />
                <Link to="/chats/{chatId}/details">
                    <button className="border rounded py-2 px-2 my-5">Details</button>
                </Link>
            </div>
        )
    }

    return (
        <div className="flex flex-col items-center col-span-2">
            <div className="text-center border rounded py-2 px-2 my-5">
                select a chat
            </div>
        </div>
    )
   
}

export default Chats