import React from 'react';
import { BasePage } from '../BaseComponent/BasePage.jsx';
import Header from "components/Header/Header.jsx";
import HeaderMockup from "components/Header/HeaderMockup.jsx";
import Footer from "components/Footer/Footer.jsx";
import Sidebar from "components/Sidebar/Sidebar.jsx";
import SidebarUser from "components/Sidebar/SidebarUser.jsx";
import dashboardRoutes from "routes/dashboard.jsx";
// @material-ui/icons
import DateRange from "@material-ui/icons/DateRange";
import 'assets/scss/material-dashboard-pro-react.css';
import cx from "classnames";

//custom scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import $ from 'jquery'
import ehealth from './i3app.js';
// var ps;
import {
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
    Survey,
    Logout,
    Note
} from 'general/Icons.js'
class EventLayoutMockup extends BasePage {
    constructor(props) {
        super(props);
        $('head').append('<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons" />');        
        $('head').append('<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">');
        $('head').append('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>');
        this.state = {
            miniActive: false,
            mobileOpen: false,
            mobileOpenUser: false,
            user: {
                name: "Đặng Tất Thắng",
                avatarUrl: "/dist/Contents/images/avatar4.jpg",
                tabs: [
                    {onClick:()=>{console.log("Edit")}, title: 'Chỉnh sửa hồ sơ',  icon: Edit},
                    {onClick:()=>{console.log("History")}, title: 'Hoạt động gần đây', icon: History},
                    {onClick:()=>{console.log("Notification")}, title: 'Thông báo', icon: Notification},
                    {onClick:()=>{this._onClick('/favoritesession')}, title: 'Chương trình yêu thích', icon: Schedule},
                    {onClick:()=>{console.log("Gamification")}, title: 'Trò chơi yêu thích', icon: Gamification},
                    {onClick:()=>{console.log("Note")}, title: 'Ghi chú', icon: Note},
                    {onClick:()=>{console.log("Survey")}, title: 'Phiếu khảo sát', icon: Survey},
                    {onClick:()=>{console.log("Logout")}, title: 'Đăng xuất', icon: Logout}
                ]
            }
        }
    }
    resizeFunction =() => {
        if (window.innerWidth >= 960) {
            this.setState({ mobileOpen: false });
        }
    }
    renderBody() {
        throw new Error("not implemented exception!");
    };

    sidebarMinimize() {
        this.setState({ miniActive: !this.state.miniActive });
    };

    handleDrawerToggle = () => {
        this.setState({ mobileOpen: !this.state.mobileOpen });
    };
    handleDrawerToggleUser = () => {
        this.setState({ mobileOpenUser: !this.state.mobileOpenUser });
    };

    componentDidMount() {
        if (navigator.platform.indexOf("Win") > -1) {
            var ps = new PerfectScrollbar(this.refs.contentPanel, {
                suppressScrollX: true,
                suppressScrollY: false
            });
            document.body.style.overflow = "hidden";
        }
        window.addEventListener("resize", this.resizeFunction);
    }
    
    _icon = function(c) {
        return (<i style={{color: '#fff'}} className={c}></i>)
    }

    _onClick = (url) => {
        console.log("EventLayout");

        //window.open(ehealth.getPath(url), '_self')
    }

    childrenRender = () => {
        let { classes, ...rest } = this.props;
        const mainPanel =
            classes.mainPanel +
            " " +
            cx({
                [classes.mainPanelSidebarMini]: this.state.miniActive,
                [classes.mainPanelWithPerfectScrollbar]:
                    navigator.platform.indexOf("Win") > -1
            });//fas fa-rss-square
        const eventRoutes = [
            { path: ehealth.getPath("/SessionList"), name: "Chương trình", icon: Schedule},
            { path: ehealth.getPath("/ActivityFeeds"), name: "Bên lề sự kiện", icon: ActivityFeed },
            { path: ehealth.getPath("/Attendees"), name: "Người tham dự", icon: Attendees },
            { path: ehealth.getPath("/Speakers"), name: "Diễn giả", icon: Speakers },
            { path: ehealth.getPath("/Documents"), name: "Tài liệu", icon: Documents },
            { path: ehealth.getPath("/Information"), name: "Thông tin", icon: Information },
            { path: ehealth.getPath("/Games"), name: "Trò chơi tương tác", icon: Gamification },
            { path: ehealth.getPath("/History"), name: "Lịch sử", icon: History },
        ]

        
        return (
            <React.Fragment>
                <div className={classes.wrapper}>
                    <Sidebar
                        routes={eventRoutes}
                        logoText={"Saigon Co-op"}
                        // logo={"../dist/assets/img/logo-white.svg"}
                        image={"/dist/assets/img/sidebar-3.jpg"}
                        handleDrawerToggle={this.handleDrawerToggle}
                        open={this.state.mobileOpen}
                        color="blue"
                        bgColor="black"
                        miniActive={this.state.miniActive}
                        {...rest}
                    />
                    <SidebarUser
                        user={this.state.user}
                        routes={[]}
                        //backgroundColor={'#313638'}
                        image={"/dist/assets/img/sidebar-3.jpg"}
                        handleDrawerToggle={this.handleDrawerToggleUser}
                        open={this.state.mobileOpenUser}
                        color="blue"
                        bgColor="black"
                        miniActive={this.state.miniActive}
                        {...rest}
                    />
                    <div className={mainPanel} ref="contentPanel">
                        <HeaderMockup
                            sidebarMinimize={this.sidebarMinimize.bind(this)}
                            miniActive={this.state.miniActive}
                            //i3 custom props
                            headerText={"SGC Event Management"}
                            headerColor={ehealth.color.red}
                            routes={eventRoutes}
                            handleDrawerToggle={this.handleDrawerToggle}
                            handleDrawerToggleUser={this.handleDrawerToggleUser}
                            {...rest}
                        />
                        <div className={classes.content} style={{ overFlow: 'hidden !important', paddingTop: '1px' }}>
                            {this.renderBody()}
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    };
}



export default EventLayoutMockup;

