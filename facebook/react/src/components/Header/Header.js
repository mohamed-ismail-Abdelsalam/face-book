import React from 'react';
import "./Header.css";
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';
import FlagIcon from '@mui/icons-material/Flag';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';
import StoreIcon from '@mui/icons-material/Store';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import {IconButton, Avatar} from '@mui/material';
import ForumIcon from '@mui/icons-material/Forum';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {Link, useLocation} from 'react-router-dom';
import {useEffect, useState} from "react";
import Badge from '@mui/material/Badge';
import axios from "axios";
import {useHistory} from "react-router-dom";
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import PopupState, { bindTrigger, bindMenu } from 'material-ui-popup-state';
import Logout from '@mui/icons-material/Logout';
import PersonAdd from '@mui/icons-material/PersonAdd';
import '../chat/Stylechat.css';



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

function Header() {
    const history = useHistory();
    const [users, setUsers] = useState({})
    const [value, setValue] = useState('')
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            history.push("/home/search/"+event.target.value)
        }
    }
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get/')
            .then(res => {
                setUsers(res.data[0]);
            })
            .catch((err) => console.log(err))
    }, [])
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
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
        <div className="header">
            <div className="header-left">
                <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/1024px-Facebook_f_logo_%282019%29.svg.png"
                    alt=""/>
                <>
                    <div className="header-input">
                        <SearchIcon/>
                        <input placeholder="Search Facebook" style={{color: 'black'}} value={value}
                            onChange={(e) => setValue(e.target.value)} onKeyDown={handleKeyDown} type="text"/>

                    </div>
                </>
            </div>
            <div className="header-center">
                <div className="header-option header-option--active">
                    <Link to={`/home/Home/`}>
                        <HomeIcon fontSize="large"/></Link>
                </div>
                <div className="header-option">
                    <FlagIcon fontSize="large"/>
                </div>
                <div className="header-option">
                    <SubscriptionsIcon fontSize="large"/>
                </div>
                <div className="header-option">
                    <StoreIcon fontSize="large"/>
                </div>
                <div className="header-option">
                    <Link to={"/home/sugistions_list/"}>
                        <SupervisorAccountIcon fontSize="large"/>
                    </Link>
                </div>
            </div>
            <div className="header-right">
                <div className="header-info">
                    <Avatar src={users.pic}/>
                    <Link to={`/home/pro/` + users.id}>
                        <h4>{users.first_name + ' ' + users.last_name}</h4></Link>
                </div>
                
                    <IconButton id="basic-button"
                        aria-controls={open ? 'basic-menu' : undefined}
                        aria-haspopup="true"
                        aria-expanded={open ? 'true' : undefined}
                        onClick={handleClick}
                        >
                        <Badge badgeContent={4} color="primary"> 
                            <ForumIcon/>
                        </Badge>
                    </IconButton>
                <IconButton>
                    <NotificationsActiveIcon/>
                </IconButton>
                <PopupState variant="popover" popupId="demo-popup-menu">
                    {(popupState) => (
                        <React.Fragment>
                        <IconButton variant="contained" {...bindTrigger(popupState)}>
                            <ExpandMoreIcon/>
                        </IconButton>
                        <Menu {...bindMenu(popupState)}>
                            <MenuItem onClick={popupState.close}><Avatar sx={{ width: 24, height: 24 }}/>  Profile</MenuItem>
                            <MenuItem onClick={popupState.close}><PersonAdd fontSize="small" />   find friends</MenuItem>
                            <MenuItem onClick={popupState.close}>
                                <Logout fontSize="small" />  Logout
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
                    <MenuItem onClick={handleClose} ><div className="chat-container">
                        <div className="header">chats</div>
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
            </div>
        </div>
    )
}

export default Header