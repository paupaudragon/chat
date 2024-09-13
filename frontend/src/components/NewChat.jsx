import { useState } from "react"
import { useMutation, useQueryClient } from "react-query"
import { useNavigate } from "react-router-dom"
import {useAuth} from "../context/auth"
import Button from "./Button"


function Input(props) {
    return (
        <div className='flex flex-row'>
            <input className="border rounded bg-transparent mx-2 py-1 px-2"{...props} />
            <Button type='submit' className='mx-2'> Send</Button>
            <Button> Detail</Button>
        </div>
    )
    
}


function NewChatForm({ chatId}) {

    const queryClient = useQueryClient();
    const navigate = useNavigate(); 
    const { token } = useAuth()

    const [text, setText] = useState("Add message here")

    const mutation = useMutation({
        mutationFn: () => (
            fetch(
                `http://127.0.0.1:8000/chats/${chatId}/messages`,
                {
                    method: "POST",
                    headers: {
                        'Authorization': "Bearer " + token,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        text
                    }) //not sending an object but a json

                }
            ).then((response)=> response.json())
    ),// no need to return because using () not {}
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["chat", `${chatId}`], 
            })
            navigate(`/chats/${chatId}`)
         },
        onError: () => { }
    })

    const onSubmit = (e) => {
        e.preventDefault(); 
        mutation.mutate()
    }
    
    return (
        <form onSubmit={onSubmit}>
            <Input
                name="message"
                type='text'
                value={text}
                onChange={((e)=>
                    setText(e.target.value)
                )}
            />
        </form>
    )
}
function NewChat({chatId}) {

    return (
        <div>
            {/* <h2>add a new message</h2> */}
            <NewChatForm chatId={chatId}></NewChatForm>
        </div>
    ); 
    
}

export default NewChat