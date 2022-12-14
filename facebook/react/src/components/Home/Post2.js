import React from 'react'
import Header from '../Header/Header';
import Sidebar from './Sidebar';
import Contacts from './Contacts';
import '../css/Home.css';
import '../css/Feed.css';
import {useEffect, useState} from "react";
import axios from "axios";
import AllPosts from '../Post/AllPosts';
import {useLocation} from "react-router-dom";
import { useDispatch, useSelector } from 'react-redux';
import { User } from '../../Store/action/User';
function Post2() {
    const location = useLocation();
    let id = location.pathname.split('/')[3]
    console.log(id)
    const [post, setPost] = useState([])
    const users = useSelector((state) => state.UserReducer.direc)
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get_one_post/'+id)
            .then(res => {
                setPost(res.data[0]);
            })
            .catch((err) => console.log(err))
    }, [])
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(User())
    }, [])
    return (
        <div className="home">
            {/* <Header/> */}
            <div className="home_body">
                <Sidebar/>
                <div className="feed">

                            
                    {
                        post.id  ? 

                                <AllPosts profilePic={post.user.pic}
                                            post_id={post.id}
                                            message={post.postcontent}
                                            timestamp={post.postdate}
                                            username={post.user.first_name + ' ' + post.user.last_name}
                                            image={post.post_photos}
                                            comments={post.post_comments}
                                            users={users}
                                />

                        : null
                    }

                </div>
                <Contacts/>
            </div>
        </div>
    )
}

export default Post2