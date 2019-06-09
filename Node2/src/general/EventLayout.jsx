import React from 'react';
import { BasePage } from '../BaseComponent/BasePage.jsx';
import HeaderWithUser from "components/Header/HeaderWithUser.jsx";
import Sidebar from "components/Sidebar/Sidebar.jsx";
import SidebarUser from "components/Sidebar/SidebarUser.jsx";
import 'assets/scss/material-dashboard-pro-react.css';
import cx from "classnames";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import $ from 'jquery'
import ehealth from './i3app.js';
import ModalComponent from '../BaseComponent/ModalComponent.jsx';
import ClonePerson from '../reactComponents/Person/ClonePerson.jsx';
import HubManager from '../general/HubManager';
import BigUpcoming from 'reactComponents/Events/BigUpcoming.jsx';
// import MyNotes from 'reactComponents/LayoutComponents/MyNotes'
import ProfileChange from '../reactComponents/Person/ProfileChange.jsx';
import PersonalEventNote from '../reactComponents/LayoutComponents/PersonalEventNote.jsx'
// var ps;
import EventNotification from '../reactComponents/Events/EventNotification.jsx';
import {
    News,
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
    Note,
    Timeline,
    SGCLogo,
    Star,
    ProfileSetting,
    Book,
} from 'general/Icons.js'
import UserTimeline from '../reactComponents/Person/UserTimeline.jsx';

class EventLayout extends BasePage {
    constructor(props) {
        super(props);
        $('head').append(`<link rel="stylesheet" type="text/css" href=${ehealth.getPath("/dist/Contents/cssLibraries/roboto-font.css")} />`);
        $('head').append(`<link rel="stylesheet" href=${ehealth.getPath("/dist/Contents/cssLibraries/fontawesome5/css/all.css")}>`);
        $('head').append(`<link rel="stylesheet" href=${ehealth.getPath("/dist/Contents/cssLibraries/icon.css)")}`);
        $('head').append(`<link rel="stylesheet" href=${ehealth.getPath("/dist/Contents/cssLibraries/icon.css)")}`);
        this.state = {
            miniActive: false,
            mobileOpen: false,
            mobileOpenUser: false,
            user: window.userInfo,
            tabs: [
                {
                    onClick: () => {
                        this.openModal("Thông tin cá nhân",
                            <ModalComponent
                                updateUser={this._updateUser}
                                data={this.state.user}
                            >
                                <ProfileChange />
                            </ModalComponent>
                        )
                    },
                    title: 'Thông tin cá nhân',
                    icon: ProfileSetting
                },
                {
                    onClick: () => {
                        this.openModal("Thông báo",
                            <ModalComponent
                                notifications={this.state.eventNotifications}
                                updateData={this._updateNotification}
                            >
                                <EventNotification />

                            </ModalComponent >

                        )
                    },
                    title: 'Thông báo',
                    icon: Notification
                },
                {
                    onClick: () => {
                        this.openModal("Lịch trình cá nhân",
                            <ModalComponent
                                upcomingSchedule={this.state.upcomingSchedule}
                                updateData={this._updateSchedule}
                                unlike={this._unlikeUpcomingSchedule}
                            >
                                <BigUpcoming
                                />
                            </ModalComponent>
                        )
                    },
                    title: "Lịch trình cá nhân",
                    icon: Star
                },
                {
                    onClick: () => {
                        this.openModal("Nhật ký",
                            <ModalComponent

                                data={this.state.personalEventNote.data}
                                updateData={this._updateNote}
                            // unlike={this._unlikeUpcomingSchedule}
                            >
                                <PersonalEventNote
                                />
                            </ModalComponent>
                        )
                    },
                    title: "Nhật ký",
                    icon: Book
                },
                {
                    onClick: () => {
                        this.alertify.confirm(
                            null,
                            "Bạn có chắc chắn muốn đăng xuất?",
                            {
                                okay: {
                                    title: 'Đăng xuất',
                                    handle: () => {
                                        ehealth.ajax.post({
                                            url: `/api/login/signout`,
                                            successCallback: (ack) => {
                                                localStorage.removeItem('event');
                                                localStorage.removeItem("jwtCodeCheck");
                                                window.open(ehealth.getPath("/"), "_self")
                                            },
                                            unsuccessFunction: (ack) => {

                                            }
                                        })
                                    }
                                },
                                cancel: "Không"
                            }
                        )
                    },
                    title: 'Đăng xuất',
                    icon: Logout
                }
            ],
            //notification
            eventNotifications: [],
            timeLine: [],
            openNotification: false,
            upcomingSchedule: [],
            eventRoutes: [],
            hideLeftMenu: false,
            personalEventNote: {
                data: null
            }
        }
        this.scrollBar = null;
        window.hubManager = new HubManager();
    }
    _updateNote = (data, callback) => {
        console.log('update note');
        console.log(data);
        this.updateObject(this.state.personalEventNote, { data: data }, () => {
            typeof callback === 'function' && callback();
        })
    }
    _unlikeUpcomingSchedule = (id) => {
        var session = this.state.upcomingSchedule.find(i => i.id == id);
        if (session == null) {
            throw new Error("Có lỗi xảy ra, không tìm thấy mục này!")
        }
        var like = {
            parentId: id,
            parentType: session.type
        }
        console.log('like');
        console.log(like);
        ehealth.ajax.post({
            url: `/api/Event/LikeSomeThing`,
            data: JSON.stringify(like),
            successCallback: (ack) => {
                console.log(ack);
                this.removeElement(this.state.upcomingSchedule, session);
                if (typeof this._deleteWhenUnlike == 'function') {
                    this._deleteWhenUnlike(id);
                } else {
                    throw ('_deleteWhenUnlike đã được sử dụng. Vui lòng chọn tên khác.');
                }
            },
            unsuccessFunction: () => {
                console.log('loi')
            },
            isNotBlockUI: true
        })
    };
    _updateUser = (data) => {
        this.updateObject(this.state.user, { ...data });
    }
    _updateSchedule = (data) => {
        console.log(data);

        // this.updateObject(this.state, { upcomingSchedule: data });
        this.mergeList(this.state.upcomingSchedule, data, (a, b) => { return a.id == b.id })

        //this.clearListAndPushNewItems(this.state.upcomingSchedule, data)
    };

    _updateTimeLine = (data) => {
        //this.mergeList(this.state.timeLine, data, (a, b) => { a.id == b.id })

        this.clearListAndPushNewItems(this.state.timeLine, data)
    };

    _updateNotification = (data) => {
        console.log(data);
        this.mergeList(this.state.eventNotifications, data, (a, b) => { return a.id == b.id })
        //this.clearListAndPushNewItems(this.state.eventNotifications, data);
    }

    resizeFunction = () => {
        if (window.innerWidth >= 960) {
            this.setState({ mobileOpen: false });
        }
    };
    renderBody() {
        throw new Error("not implemented exception!");
    };
    _viewNotification = () => {
        this.setState(state => ({ openNotification: !state.openNotification }
        ));
    };
    _notificationClose = () => {
        this.setState({ openNotification: false });
    };

    _getEventListLayout = () => {

        let _getPath = (path, eventId) => {
            return window.isLogin ? ehealth.getPath(path + "?eventId=" + eventId) : ehealth.getPath("/Login?eventid=" + eventId);
        }

        let event = JSON.parse(localStorage.getItem("event"));

        if (event == null) {
            return;
        }
        let eventId = event.id;
        let l = [
            {
                path: _getPath("/Event", eventId),
                name: event.name,
                icon: () => { return (<img src={event.iconUrl} style={{ width: '30px', height: '30px' }} />) },
                parent: true,
            },
            { path: _getPath("/SessionList", eventId), name: "Chương trình", icon: Schedule, parent: false },
            { path: _getPath("/ActivityFeeds", eventId), name: /*"Hoạt động bên lề"*/ "5 định hướng của SGC", icon: ActivityFeed, parent: false },
            { path: _getPath("/Games", eventId), name: /*"Trò chơi tương tác"*/ "Đấu giá gây quỹ vì cộng đồng", icon: Gamification, parent: false },
            { path: _getPath(/*"/History"*/ "/Yearbook", eventId), name: "Kỷ yếu 30 năm", icon: Book, parent: false },
            { path: _getPath("/Information", eventId), name: "Thông tin chung", icon: Information, parent: false },
            { path: _getPath("/News", eventId), name: "Tin tức Saigon Co.op", icon: News, parent: false },
            { path: _getPath("/Attendees", eventId), name: "Khách mời", icon: Attendees, parent: false },
            //{ path: _getPath("/Speakers", eventId), name: "Diễn giả", icon: Speakers, parent: false },
            //            { path: _getPath("/Documents", eventId), name: "Tài liệu", icon: Documents, parent: false },
        ];
        this.mergeList(this.state.eventRoutes, l, () => { return false; });
    }
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
        window.addEventListener("resize", this.resizeFunction);
        $('#contentDom').css('overflow', 'hidden')
        this._getEventListLayout();
    }

    _icon = function (c) {
        return (<i style={{ color: '#fff' }} className={c}></i>)
    }

    _toggleModal = (title, data, Component) => {
        this.openModal(
            title,
            title == "Thông tin cá nhân" ? <ClonePerson
                user={data}
            /> :
                <ModalComponent
                    games={data}
                    data={data}
                    disableAddFavorite
                    bgColor
                >
                    <Component

                    />
                </ModalComponent>
            , null
            , title == "Trò chơi yêu thích" ? { disablePadding: true } : {}
        )
    }



    childrenRender = () => {
        let { classes, ...rest } = this.props;
        const mainPanel =
            classes.mainPanel +
            " " +
            cx({
                [classes.mainPanelSidebarMini]: this.state.miniActive
            });//fas fa-rss-square
        const contentPanel = cx({
            [classes.mainPanelWithPerfectScrollbar]:
                navigator.platform.indexOf("Win") > -1
        })
        const { eventRoutes } = this.state;
        return (
            <React.Fragment>
                <div className={classes.wrapper}>
                    {/* <div id={`scrollTopButton`} style={{position: 'absolute', bottom: '10px', right: '16px'}}>
                        <i style={{fontSize: '45px', color: 'rbga(184, 18, 32, .6)'}} className="fas fa-angle-up"></i>
                    </div> */}
                    <Sidebar
                        routes={eventRoutes}
                        logo={ehealth.getPath("/dist/Contents/images/sgc-logo.png")}
                        logoText={"Saigon Co.op Events"}
                        image={ehealth.getPath("/dist/assets/img/sidebar-3.jpg")}
                        handleDrawerToggle={this.handleDrawerToggle}
                        open={this.state.mobileOpen}
                        color="blue"
                        bgColor="black"
                        miniActive={this.state.miniActive}
                        {...rest}
                    />
                    <SidebarUser
                        user={this.state.user}
                        tabs={this.state.tabs}
                        routes={[]}
                        image={ehealth.getPath("/dist/assets/img/sidebar-3.jpg")}
                        handleDrawerToggle={this.handleDrawerToggleUser}
                        open={this.state.mobileOpenUser}
                        color="blue"
                        bgColor="black"
                        miniActive={this.state.miniActive}
                        {...rest}
                    />
                    <div className={mainPanel} style={{ /*overFlow: 'hidden !important'*/ }}>
                        <HeaderWithUser
                            sidebarMinimize={this.sidebarMinimize.bind(this)}
                            miniActive={this.state.miniActive}
                            //i3 custom props
                            viewNotification={this._viewNotification}
                            headerText={this.state.pageTitle ? this.state.pageTitle : "Quản lý sự kiện"}
                            headerColor={ehealth.color.red}
                            routes={eventRoutes}
                            user={this.state.user}
                            tabs={this.state.tabs}
                            handleDrawerToggle={this.handleDrawerToggle}
                            handleDrawerToggleUser={this.handleDrawerToggleUser}
                            //notification props
                            viewNotification={this._viewNotification}
                            notificationClose={this._notificationClose}
                            openNotification={this.state.openNotification}
                            eventId={this.props.eventId}
                            hideLeftMenu={this.state.hideLeftMenu}
                            {...rest}
                        />
                        <div className={classes.content} id="contentPanel" style={{ paddingTop: '1px' }}>
                            {this.renderBody()}
                        </div>

                    </div>
                </div>
            </React.Fragment>
        );
    };
}



export default EventLayout;

