import React, {Fragment} from 'react';
import { withStyles, Grid } from '@material-ui/core';
import GridContainer from 'components/Grid/GridContainer.jsx';
import GridItem from 'components/Grid/GridItem.jsx';

class NavBar extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        let {classes, onClickHome, onClickNoti, onClickProfile, onClickAbout, currentTab, notiCount} = this.props;
        return(
            <Fragment>
                <div className={classes.navBar}>
                    <GridContainer style={{height: '100%', justifyContent: 'center', alignItems: 'center'}}>
                        <GridItem xs={3} style={{padding: '0'}}>
                            <div className={classes.navBtn} onClick={onClickHome} style={currentTab==0?{color: "#006bf0"}:null}>
                                <i className="fas fa-home"></i>
                                <p>Trang Chủ</p>
                            </div>
                        </GridItem>
                        <GridItem xs={3} style={{padding: '0'}}>
                            <div className={classes.navBtn} onClick={onClickNoti} style={currentTab==1?{color: "#006bf0"}:null}>
                                <i className="fas fa-bell"></i>
                                <sup>{notiCount}</sup>
                                <p>Thông báo</p>
                            </div>
                        </GridItem>
                        <GridItem xs={3} style={{padding: '0'}}>
                            <div className={classes.navBtn} onClick={onClickProfile} style={currentTab==2?{color: "#006bf0"}:null}>
                                <i className="fas fa-user"></i>
                                <p>Cá nhân</p>
                            </div>
                        </GridItem>
                        <GridItem xs={3} style={{padding: '0'}}>
                            <div className={classes.navBtn} onClick={onClickAbout} style={currentTab==3?{color: "#006bf0"}:null}>
                                <i className="fas fa-info-circle"></i>
                                <p>Về eWash</p>
                            </div>
                        </GridItem>
                    </GridContainer>
                </div>
            </Fragment>
        )
    }
}
const styles = {
    navBar: {
        position: 'fixed',
        height: '50px',
        bottom: '0',
        width: '100%',
        borderTop: '1px solid lightgray',
        backgroundColor: 'white',
        color: '#667'
    },
    navBtn: {
        '& p': {
            margin: '0',
            textAlign: 'center',
            fontSize: '.75rem'
        },
        textAlign: 'center'
    }
}

export default withStyles(styles)(NavBar);