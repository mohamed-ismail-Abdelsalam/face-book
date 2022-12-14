import React from 'react';
import "./Header.css";
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';
import FlagIcon from '@mui/icons-material/Flag';
import StoreIcon from '@mui/icons-material/Store';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import { IconButton, Avatar } from '@mui/material';
import ForumIcon from '@mui/icons-material/Forum';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Link} from 'react-router-dom';
import { useEffect, useState } from "react";
import Badge from '@mui/material/Badge';
import axios from "axios";
import { useHistory } from "react-router-dom";
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import PopupState, { bindTrigger, bindMenu } from 'material-ui-popup-state';
import Logout from '@mui/icons-material/Logout';
import PersonAdd from '@mui/icons-material/PersonAdd';
import '../chat/Stylechat.css';
import GroupsIcon from '@mui/icons-material/Groups';
import Button from '@mui/material/Button';
import CancelIcon from '@mui/icons-material/Cancel';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import {useDispatch, useSelector} from 'react-redux';
import {User} from '../../Store/action/User';
import {useLocation} from "react-router-dom";


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function Header() {
    const history = useHistory();
    const [value, setValue] = useState('')
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            let temp = event.target.value
            document.getElementById("searchinput").value = ""
            history.push("/home/search/" + temp)
        }
    }
    const [activehome , setactivehome]=useState('')
    const [activegroup , setactivegroup]=useState('')
    const [activelist , setactivelist]=useState('')
    let location = useLocation();
    let checkactive= location.pathname.split('/')[2]
    useEffect(() => {
        if (checkactive === "Home"){
            setactivehome("header-option--active")
            setactivegroup("")
            setactivelist("")
        }
        else if (checkactive === "groups" || checkactive === "group") {
            setactivegroup("header-option--active")
            setactivehome("")
            setactivelist("")
        }else if (checkactive === "sugistions_list"){
            setactivelist("header-option--active")
            setactivehome("")
            setactivegroup("")
        }
    },[checkactive])
    const users = useSelector((state) => state.UserReducer.direc)
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(User())
    },[])
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    const [NotifyEl, setNotifyEl] = useState(null);
    const openNotify = Boolean(NotifyEl);
    const handleClickNotify = (event) => {
        setNotifyEl(event.currentTarget);
    };
    const handleCloseNotify = () => {
        setNotifyEl(null);
    };
    const [friends, setfriends] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/friends_list_chat/')
            .then(res => {
                setfriends(res.data);
            })
            .catch((err) => console.log(err))
    }, [])
    const [Invisib, setInvisib] = useState(true)
    // const getNotification = () => {
    //     let url = "http://127.0.0.1:8000/api/chatNotification/"
    //     axios.get(url)
    //         .then(res => res.json())
    //         .then(data => {
    //             let cou = 0
    //             let chatNotificationBtn = document.getElementsByClassName("msg")
    //             for (let i = 0; i < data.length; i++) {
    //                 if (data[i] === 0) {
    //                     cou = cou + 0
    //                 } else {
    //                     cou = cou + 1
    //                     if (anchorEl === null) {
    //                     } else {
    //                         chatNotificationBtn[i].innerText = data[i]
    //                     }
    //                 }
    //             }
    //             if (cou === 0) {
    //                 setInvisib(true)
    //             } else {
    //                 setInvisib(false)
    //             }
    //         })
    //         .catch(error => {})
    // }
    const [notifications, setNotifications] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/postNotification/')
            .then(res => {
                setNotifications(res.data);
            })
            .catch((err) => console.log(err))
    }, [notifications])
    const [InviteNotive, setInviteNotive] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/inviteNotification/')
            .then(res => {
                setInviteNotive(res.data);
            })
            .catch((err) => console.log(err))
    }, [InviteNotive])

    const [notifyRequest, setnotifyRequest] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/notifyRequest/')
            .then(res => {
                setnotifyRequest(res.data);
            })
            .catch((err) => console.log(err))
    }, [notifyRequest])
    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/chatNotification/")
            .then(res => {
                let data = res.data
                let cou = 0
                let chatNotificationBtn = document.getElementsByClassName("msg")
                for (let i = 0; i < res.data.length; i++) {
                    if (data[i] === 0) {
                        cou = cou + 0
                    } else {
                        cou = cou + 1
                        if (anchorEl === null) {
                        } else {
                            chatNotificationBtn[i].innerText = data[i]
                        }
                    }
                }
                if (cou === 0) {
                    setInvisib(true)
                } else {
                    setInvisib(false)
                }
            })
            .catch(error => {})
    }, [notifyRequest])
    function renderTimestamp(timestamp) {
        let prefix = "";
        const timeDiff = Math.round(
            (new Date().getTime() - new Date(timestamp).getTime()) / 60000
        );
        if (timeDiff < 1) {
            // less than one minute agog
            prefix = "just now...";
        } else if (timeDiff < 60 && timeDiff >= 1) {
            // less than sixty minutes ago
            prefix = `${timeDiff} minutes ago`;
        } else if (timeDiff < 24 * 60 && timeDiff > 60) {
            // less than 24 hours ago
            prefix = `${Math.round(timeDiff / 60)} hours ago`;
        } else if (timeDiff < 31 * 24 * 60 && timeDiff > 24 * 60) {
            // less than 7 days ago
            prefix = `${Math.round(timeDiff / (60 * 24))} days ago`;
        } else {
            prefix = `${new Date(timestamp)}`;
        }
        return prefix;
    }
    const frined_request_delete_notify = (notify_id,sender_id) => {
        const datarequest = {
            notify_id: parseInt(notify_id),
            sender_id: parseInt(sender_id),
            user_id:parseInt(users.id),
        }
        axios.post("http://127.0.0.1:8000/api/frined_request_delete_notify/",
        datarequest, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        },
        ).then(res => {
            history.push("/home/Home/")
            axios.get('http://127.0.0.1:8000/api/notifyRequest/')
            .then(res => {
                setnotifyRequest(res.data);
            })
            .catch((err) => console.log(err))
        }).catch((err) => console.log(err))
    }
    const frined_request_accept_notify = (notify_id,sender_id) => {
        const datarequest = {
            notify_id: parseInt(notify_id),
            sender_id: parseInt(sender_id),
            user_id:parseInt(users.id),
        }
        axios.post("http://127.0.0.1:8000/api/frined_request_accept_notify/",
        datarequest, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        },
        ).then(res => {
            history.push("/home/Home/")
            axios.get('http://127.0.0.1:8000/api/notifyRequest/')
            .then(res => {
                setnotifyRequest(res.data);
            })
            .catch((err) => console.log(err))
        }).catch((err) => console.log(err))
    }
    // setInterval(getNotification, 2000)
    return (
            <div className="header">
            <div className="header-left">
                <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/1024px-Facebook_f_logo_%282019%29.svg.png"
                    alt=""
                    style={{ marginTop: "12px" }} />
                <>
                    <div className="header-input">
                        <SearchIcon />
                        <input placeholder="Search Facebook" style={{ color: 'black' }} value={value} id="searchinput"
                            onChange={(e) => setValue(e.target.value)} onKeyDown={handleKeyDown} type="text" />
                    </div>
                </>
            </div>
            <div className="header-center">
                <div className={"header-option "+ activehome }>
                    <Link to={`/home/Home/`}>
                        <HomeIcon fontSize="large" /></Link>
                </div>
                <div className="header-option ">
                    <FlagIcon fontSize="large" />
                </div>
                <div className={"header-option "+ activegroup }>
                    <Link to={`/home/groups/`}>

                        <GroupsIcon fontSize="large" /></Link>
                </div>
                <div className="header-option">

                    <StoreIcon fontSize="large" />

                </div>
                <div className={"header-option "+ activelist }>
                    <Link to={"/home/sugistions_list/"}>
                        <SupervisorAccountIcon fontSize="large" />
                    </Link>
                </div>
            </div>
            <div className="header-right">
                <div className="header-info">
                    <Avatar src={users.pic} />
                    <Link to={`/home/pro/` + users.id}>
                        <h4>{users.first_name + ' ' + users.last_name}</h4></Link>
                </div>

                <IconButton id="basic-button"
                    aria-controls={open ? 'basic-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? 'true' : undefined}
                    onClick={handleClick}
                    style={{ marginTop: "15px" }}
                >
                    <Badge variant="dot" invisible={Invisib} color="primary">
                        <ForumIcon />
                    </Badge>
                </IconButton>
                <IconButton id="basic-button-notify"
                    aria-controls={openNotify ? 'basic-menu-notify' : undefined}
                    aria-haspopup="true"
                    aria-expanded={openNotify ? 'true' : undefined}
                    onClick={handleClickNotify}
                    style={{ marginTop: "15px" }}
                >

                    <Badge badgeContent={notifications.length + InviteNotive.length + notifyRequest.length} color="primary">
                        <NotificationsActiveIcon />

                    </Badge>
                </IconButton>
                <PopupState variant="popover" popupId="demo-popup-menu">
                    {(popupState) => (
                        <React.Fragment>

                            <IconButton variant="contained" {...bindTrigger(popupState)} style={{ marginTop: "15px" }}>
                                <ExpandMoreIcon />

                            </IconButton>
                            <Menu {...bindMenu(popupState)}>
                                <MenuItem onClick={popupState.close}> <a href={"/home/pro/" + users.id}><Avatar
                                    sx={{ width: 24, height: 24 }} /> Profile </a></MenuItem>
                                <MenuItem onClick={popupState.close}> <a href={"/home/sugistions_list/"}> <PersonAdd
                                    fontSize="small" /> find friends </a></MenuItem>
                                <MenuItem onClick={popupState.close}>
                                    <a href="/auth/logout/"> <Logout fontSize="small" /> Logout </a>
                                </MenuItem>
                            </Menu>
                        </React.Fragment>
                    )}
                </PopupState>
                <Menu
                    id="basic-menu"
                    anchorEl={anchorEl}
                    open={open}
                    onClose={handleClose}
                    MenuListProps={{
                        'aria-labelledby': 'basic-button',
                    }}
                >
                    <MenuItem onClick={handleClose}>
                        <div className="chat-container">
                            <div className="header">chats</div>
                            <div className="friends-container">
                                {
                                    friends.map((friend) => {
                                        return <>
                                            <a href={'/chats/detail/' + friend.id}
                                                style={{ color: "black", textDecoration: "none" }}>
                                                <div className="friends">
                                                    <div className="pic">
                                                        <img src={friend.pic} alt="" />
                                                    </div>
                                                    <div className="name">
                                                        <h5>{friend.first_name + ' ' + friend.last_name}</h5>
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
                        </div>
                    </MenuItem>
                </Menu>
                <Menu
                    id="basic-menu-notify"
                    anchorEl={NotifyEl}
                    open={openNotify}
                    onClose={handleCloseNotify}
                    MenuListProps={{
                        'aria-labelledby': 'basic-button-notify',
                    }}
                >
                    <MenuItem onClick={handleCloseNotify}>
                        <div className="chat-container" >
                            <div className="header">Notifications</div>
                            <div className="friends-container">
                                {
                                    notifications.map((notify) => {
                                        return <>
                                            <a href={'/api/unseenNotification/' + notify.id + '/' + notify.post}
                                                style={{ color: "black", textDecoration: "none" }}>
                                                <div className="friends">
                                                    <div className="pic">
                                                      <img src={notify.user.pic} alt="" />
                                                    </div>
                                                    <div className="name">
                                                        <h4>{notify.user.first_name + " " + notify.user.last_name}</h4>
                                                        <h5>{notify.body}</h5>
                                                    </div>
                                                    <div className="time_new_msg">
                                                        <p>{renderTimestamp(notify.timestamp)}</p>

                                                    </div>
                                                </div>
                                            </a>
                                        </>
                                    })
                                }
                                {
                                    InviteNotive.map((notify) => {
                                        return <>
                                            <a href={'/api/unseeninviteNotification/' + notify.id + '/' + notify.group}
                                               style={{color: "black", textDecoration: "none"}}>
                                                <div className="friends">
                                                    <div className="pic">
                                                        <img src={notify.user.pic} alt=""/>
                                                    </div>
                                                    <div className="name">
                                                        <h4>{notify.user.first_name + " " + notify.user.last_name}</h4>
                                                        <h5>{notify.body}</h5>
                                                    </div>
                                                    <div className="time_new_msg">
                                                        <p>{renderTimestamp(notify.timestamp)}</p>

                                                    </div>
                                                </div>
                                            </a>
                                        </>
                                    })
                                }
                                {
                                    InviteNotive.map((notify) => {
                                        return <>
                                            <a href={'/api/unseeninviteNotification/' + notify.id + '/' + notify.group}
                                                style={{ color: "black", textDecoration: "none" }}>
                                                <div className="friends">
                                                    <div className="pic">
                                                        <img src={notify.user.pic} alt="" />
                                                    </div>
                                                    <div className="name">
                                                        <h4>{notify.user.first_name + " " + notify.user.last_name}</h4>
                                                        <h5>{notify.body}</h5>
                                                    </div>
                                                    <div className="time_new_msg">
                                                        <p>{renderTimestamp(notify.timestamp)}</p>
                                                    </div>
                                                </div>
                                            </a>
                                        </>
                                    })
                                }
                                {
                                    notifyRequest.map((notify) => {
                                        return <>
                                            {/* href={'/api/unseennotifyRequest/' + notify.id + '/' + notify.user.id}
                                            <a style={{ color: "black", textDecoration: "none" }}> */}
                                            <div className="friends ">
                                                <a href={'/api/unseennotifyRequest/' + notify.id + '/' + notify.user.id} style={{ color: "black", textDecoration: "none" }}>
                                                    <div className="pic">
                                                        <img src={notify.user.pic} alt="" />
                                                    </div>
                                                </a>
                                                <div className="name">
                                                    <h4>{notify.user.first_name + " " + notify.user.last_name}</h4>
                                                    <h5>{notify.body}</h5>
                                                    <div className="d-flex flex-row align-items-center px-3 py-1 ">
                                                        <span className="friend-text align-items-center mr-2">Friend Request</span>
                                                            <Button onClick={(notify_id,sender_id)=>{frined_request_delete_notify(notify.id,notify.user.id)}} >
                                                                <CancelIcon />
                                                            </Button>
                                                        <Button onClick={(notify_id,sender_id)=>{frined_request_accept_notify(notify.id,notify.user.id)}}>
                                                            <CheckCircleIcon />
                                                        </Button>
                                                    </div>
                                                </div>
                                                <div className="time_new_msg">
                                                    <p>{renderTimestamp(notify.timestamp)}</p>
                                                </div>
                                            </div>
                                            {/* </a> */}
                                        </>
                                    })
                                }
                            </div>
                        </div>
                    </MenuItem>
                </Menu>
            </div>
        </div>
           
    )
}

export default Header