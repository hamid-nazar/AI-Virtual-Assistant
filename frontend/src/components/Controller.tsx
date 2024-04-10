import React, { useState } from 'react'
import { Title } from './Title'
import { RecordMessage } from './RecordMessage'
import axios from 'axios'



export function Controller() {

  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState<any[]>([])
  let blob = new Blob();

  function createBlobURL(data: any) {

    const blob = new Blob([data], { type: "audio/mpeg" });

    const url = window.URL.createObjectURL(blob);

    return url;
  }

  async function handleStop(blobUrl: string) {

    setIsLoading(true)

    try {


      const myMessage = { sender: "me", blobUrl };
      const messagesArr = [...messages, myMessage];

      const response = await fetch(blobUrl);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append('file', blob, 'myFile.wav');


      const res = await axios.post('http://localhost:8000/audio', formData,
        {
          headers:
          {
            'Access-Control-Allow-Origin': '*',
            "Content-Type": "audio/mpeg",
          },
          responseType: "arraybuffer"
        })

      const adamMessage = { sender: "adam", blobUrl: createBlobURL(res.data) }

      messagesArr.push(adamMessage)

      setMessages(messagesArr)

      console.log(messages.length)

      const audio = new Audio(adamMessage.blobUrl);

      setIsLoading(false)
      
      audio.play();

     

    } catch (error) {

      console.log(error)

      setIsLoading(false)
    }


  }


  return (
    <div className='h-screen y-overflow-hidden'>
      <Title setMessages={setMessages} setColor={"bg-gray-900"} />

      <div className='flex flex-col justify-between h-full overflow-y-scroll pb-96'>

        {/* conversation */}

        <div className='mt-5 px-5'>

          {messages.map(function (audio, index) {
            return (<div key={index + audio.sender}
              className={"flex flex-col " + (audio.sender == "adam" && "flex items-end")}>
              <div className='mt-4'>
                <p className={audio.sender == "adam" ? "text-right mr-2 italic text-green-500" : "ml-2 italic text-blue-500"}>
                  {audio.sender}
                </p>

                {/* Message */}
                <audio src={audio.blobUrl} className="appearance-none" controls />

              </div>
            </div>)
          })}

          {messages.length == 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send Adam a message...
            </div>)}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Gimme a few seconds...
            </div>
          )}

        </div>

        <div className='fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500'>
          <div className='flex justify-center items-center w-full'>

            <RecordMessage handleStop={handleStop} />

          </div>
        </div>

      </div>
    </div>
  )
}
