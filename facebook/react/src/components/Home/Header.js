import React from 'react';
import "../css/Header.css";
import facelogo from '../images/facelogo.png';
import SearchIcon from '@mui/icons-material/Search';
import HomeIcon from '@mui/icons-material/Home';
import FlagIcon from '@mui/icons-material/Flag';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';
import StoreIcon from '@mui/icons-material/Store';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import {IconButton, Avatar} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ForumIcon from '@mui/icons-material/Forum';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {useLocation, Link} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

function Header({name, image}) {

    let location = useLocation();
    let id = location.pathname.split('/')[3]
    const [users, setUsers] = useState({})

    useEffect(() => {

        axios.get('http://127.0.0.1:8000/api/get/' + id)

            .then(res => {

                setUsers(res.data[0]);


            })

            .catch((err) => console.log(err))

    }, [])
    return (
        <div className="header">
            <div className="header-left">
                <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Facebook_f_logo_%282019%29.svg/1024px-Facebook_f_logo_%282019%29.svg.png"
                    alt=""/>
                <div className="header-input">
                    <SearchIcon/>
                    <input placeholder="Search Facebook" type="text"/>
                </div>
            </div>
            <div className="header-center">

                <div className="header-option header-option--active">
                    <Link to={`/chats/Home/${id}`}>
                        <HomeIcon fontSize="large"/>
                    </Link>
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
                    <SupervisorAccountIcon fontSize="large"/>
                </div>
            </div>
            <div className="header-right">
                <div className="header-info">
                    <Avatar src={image}/>
                    <h4>{name}</h4>
                </div>
                <IconButton>
                    <ForumIcon/>
                </IconButton>
                <IconButton>
                    <NotificationsActiveIcon/>
                </IconButton>
                <IconButton>
                    <ExpandMoreIcon/>
                </IconButton>
            </div>
        </div>
    )
}

export default Header