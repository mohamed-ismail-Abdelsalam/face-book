import React from 'react';
import {useEffect, useState} from "react";
import CSRF from "../Auth/CSRF";
import axios from "axios";
import './Stylechat.css';

function getNotification(){
    let url = "http://127.0.0.1:8000/api/chatNotification/"
    fetch(url)
    .then(res=>res.json())
    .then(data=>{
        // console.log(data)
        let chatNotificationBtn = document.getElementsByClassName("msg")
        for(let i = 0; i<data.length; i++){
            chatNotificationBtn[i].innerText = data[i]
        }
    })
    .catch(error => console.log(error))
}

function Index() {
    const [user,setuser]=useState([])
    // const [friends,setfriends]=useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get/')
            .then(res => {
                setuser(res.data[0]);
            })
            .catch((err) => console.log(err))
    }, [])
    // useEffect(() => {
    //     axios.get('http://127.0.0.1:8000/api/chatIndex/')
    //         .then(res => {
    //             setfriends(res.data);
    //             console.log(res.data);
    //         })
    //         .catch((err) => console.log(err))
    // }, [])
    const [friends, setfriends] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/friends_list_chat/')
            .then(res => {
                setfriends(res.data);
            })
            .catch((err) => console.log(err))
    }, [])
    setInterval(getNotification, 1000)
    return (
        <>
            <div className="chat-container">
                <div className="mainChat">
                <div className="logochat">
                    ChatMe
                </div>
                <div className="sub-main">
                    <div className="main-user">
                        <img src={user.pic} alt="profile picture" />
                    </div>
                    <p>@{user.first_name}</p>
                </div>
                </div>
                <div className="header">Messages</div>
                <div className="friends-container">
                    {
                        friends.map((friend)=>{
                            return <>
                                <a href={'/chats/detail/'+ friend.id} style={{color:"black", textDecoration: "none"}}>
                                    <div className="friends">
                                        <div className="pic">
                                        <img src={friend.pic} alt="" />
                                        </div>
                                        <div className="name">
                                        <h5>{friend.first_name+ ' ' + friend.last_name}</h5>
                                        <p>How are you doing today</p>
                                        </div>
                                        <div className="time_new_msg">
                                            <p>7:30am</p> 
                                        <div className="msg">0</div>
                                        </div>
                                    </div>
                                </a>
                            </>
                        })
                    }
                </div>
                <div className="chatfooter">
                <div>
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="26"
                    height="26"
                    fill="currentColor"
                    className="bi bi-person-plus"
                    viewBox="0 0 16 16"
                    >
                    <path
                        d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"
                    />
                    <path
                        fill-rule="evenodd"
                        d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"
                    />
                    </svg>
                </div>
            
                <div>
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="26"
                    height="26"
                    fill="currentColor"
                    className="bi bi-house"
                    viewBox="0 0 16 16"
                    >
                    <path
                        fill-rule="evenodd"
                        d="M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"
                    />
                    <path
                        fill-rule="evenodd"
                        d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"
                    />
                    </svg>
                </div>
            
                <div>
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="26"
                    height="26"
                    fill="currentColor"
                    className="bi bi-gear"
                    viewBox="0 0 16 16"
                    >
                    <path
                        d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"
                    />
                    <path
                        d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"
                    />
                    </svg>
                </div>
                </div>
            </div>
        </>
    )
}

export default Index