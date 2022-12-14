import React from 'react';
import '../css/Home.css';
import Feed from './Feed';
import Sidebar from './Sidebar';
import Contacts from './Contacts';


function Home() {
    return (
        <div className="home">
            <div className="home_body">
                <Sidebar/>
                <Feed/>
                <Contacts/>
            </div>
        </div>
    );
}

export default Home;
