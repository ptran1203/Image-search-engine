import React from "react";
import ehealth from 'general/i3app'
var generateIcon = (fasClassName, props) => {
  return (<i style={{...props}} className={fasClassName}></i>)
}
var generateNumberIcon = (n) => {
  return (
    <React.Fragment>
      <span style={{fontSize: '15px', fontWeight: '400'}}>{"Th3"}</span>
      <span style={{fontSize: '15px', fontWeight: '400'}}>{n}</span>
    </React.Fragment>
  )
}
var sgcLogo = function(){
  return(
    <img style={{width: '30px', height: '30px'}} src={ehealth.getPath("/dist/Contents/images/Logo.png")}/> 
  )
}
var Schedule = generateIcon.bind(this,"fas fa-calendar-alt");
var ActivityFeed = generateIcon.bind(this, "fas fa-rss-square");
var Attendees = generateIcon.bind(this, "fas fa-users");
var Speakers = generateIcon.bind(this, "fas fa-chalkboard-teacher");
var Documents = generateIcon.bind(this, "fas fa-file");
var Information = generateIcon.bind(this, "fas fa-info-circle");
var Gamification = generateIcon.bind(this, "fas fa-trophy");
var Edit = generateIcon.bind(this, "fas fa-edit")
var History = generateIcon.bind(this, "fas fa-history")
var Notification = generateIcon.bind(this, "fas fa-bell")
var Star = generateIcon.bind(this, "fas fa-star")
var Survey = generateIcon.bind(this, "fas fa-poll-h")
var Logout = generateIcon.bind(this, "fas fa-sign-out-alt")
var Note = generateIcon.bind(this, "fas fa-sticky-note")
var Timeline = generateIcon.bind(this, "fas fa-birthday-cake")
var News = generateIcon.bind(this, "fas fa-newspaper")
var Search = generateIcon.bind(this, "fas fa-search")
var PointInMap = generateNumberIcon.bind(this, 2019);
var SGCLogo = sgcLogo.bind(this);
var ProfileSetting = generateIcon.bind(this, "fas fa-user-cog");
var Book = generateIcon.bind(this, "fas fa-book")

export {
  Schedule, 
  ActivityFeed, 
  Attendees, 
  Speakers, 
  Documents, 
  Information, 
  Gamification,
  Edit,
  History, 
  Notification,
  Star,
  Survey,
  Logout,
  Note,
  Timeline,
  News,
  Search,
  PointInMap,
  SGCLogo,
  ProfileSetting,
  Book
};

