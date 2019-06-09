import React from 'react';
import { BasePage } from '../BaseComponent/BasePage.jsx';
import 'assets/scss/material-dashboard-pro-react.css';
import cx from "classnames";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import $ from 'jquery'
import ehealth from './i3app.js';
import HubManager from './HubManager';
import GridContainer from 'components/Grid/GridContainer.jsx';
import GridItem from 'components/Grid/GridItem.jsx';
class AdminLayout extends BasePage {
    constructor(props) {
        super(props);
        $('head').append(`<link rel="stylesheet" type="text/css" href=${ehealth.getPath("/dist/Contents/cssLibraries/roboto-font.css")} />`);
        $('head').append(`<link rel="stylesheet" href=${ehealth.getPath("/dist/Contents/cssLibraries/fontawesome5/css/all.css")}>`);
        $('head').append(`<link rel="stylesheet" href=${ehealth.getPath("/dist/Contents/cssLibraries/icon.css)")}`);
        this.state = {
            miniActive: false,
            mobileOpen: false,
            mobileOpenUser: false
        }
        this.scrollBar = null;
        window.hubManager = new HubManager();
    }
    resizeFunction = () => {
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
        
        document.body.style.overflowY = "auto"
    }

    childrenRender = () => {
        let { classes, ...rest } = this.props;

        return (
            <React.Fragment>
                <GridContainer justify="center">
                    <GridItem md={10} xs={12} sm={12}>
                        <div style={{ marginTop: '40px' }} id="contentPanel">
                            {this.renderBody()}
                        </div>
                    </GridItem>
                </GridContainer>
            </React.Fragment>
        );
    };
}



export default AdminLayout;

