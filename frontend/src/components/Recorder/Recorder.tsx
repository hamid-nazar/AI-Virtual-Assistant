import React, { useState } from "react";


import "./Recorder.css";
import { RecordIcon } from "../RecordIcon";
import { RecordMessage } from "../RecordMessage";
import axios from "axios";
import { Title } from "../Title";



export function Recorder() {

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

      // messagesArr.push(adamMessage)

      // setMessages(messagesArr)

      // console.log(messages.length)

      const audio = new Audio(adamMessage.blobUrl);

      setIsLoading(false)

      if(response.status === 200){

        audio.play();
      }
    

    } catch (error) {

      console.log(error)

      setIsLoading(false)
    }


  }



  return (
    <>
    <Title setMessages={setMessages} setColor={"bg-gray-500 "}/>
    <div className="main">
      
      <div className="image-container">
        <div className="image">
          <img src="robot.gif" alt="image"  className="rounded-full"/>
          {/* <video autoPlay loop muted playsInline className="h-60 w-96">
            <source src="ai.mp4" type="video/mp4" />
          </video> */}
        </div>
        <h1>Rachel</h1>
        <p>I'm a Virtual Assistant Rachel, How may I help you?</p>
      </div>
      <div className="input cursor-pointer">
        <button className="talk">
          {/* <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6 cursor-pointer">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
          </svg> */}
          <RecordMessage handleStop={handleStop} />
          </button>
        <h1 className="content">{isLoading ? "Loading..." :" Click here to speak"}</h1>
      </div>
    </div>
    </>
  );
}
