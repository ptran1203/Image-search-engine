import React from 'react';
import {BasePage} from '../BaseComponent/BasePage.jsx';
import 'assets/scss/material-dashboard-pro-react.css';
import cx from "classnames";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
//custom scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import $ from 'jquery'
// var ps;
class TestLayout extends BasePage {
    constructor(props) {
        super(props);
        $('head').append('<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons" />');
        $('head').append('<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">');
        this.state = {
            miniActive: false,
            mobileOpen: false
        }
        this.resizeFunction = this.resizeFunction.bind(this);
    }
    resizeFunction() {
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


    childrenRender = () => {
        let { classes } = this.props;
        const mainPanel = 
            cx({
                [classes.mainPanelSidebarMini]: this.state.miniActive,
                [classes.mainPanelWithPerfectScrollbar]:
                    navigator.platform.indexOf("Win") > -1
            });
        return (
            <React.Fragment>
                <div ref="contentPanel">
                    <GridContainer justify="center">
                        <GridItem md={10} xs = {12} sm ={12}>
                            <div className={classes.wrapper}>
                                <div className={mainPanel} ref="contentPanel">
                                    <div className={classes.content} style={{ overFlow: 'hidden !important' }}>
                                        {this.renderBody()}
                                    </div>
                                </div>
                            </div>
                        </GridItem>
                    </GridContainer>
                </div>
            </React.Fragment>
        );
    };
}



export default TestLayout;

